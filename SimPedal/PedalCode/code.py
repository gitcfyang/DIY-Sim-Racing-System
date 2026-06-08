# ================================================
# code.py
# GT3 模拟器踏板主程序
#
# 硬件：
#   RP2040 (Raspberry Pi Pico)
#   霍尔传感器 x2：
#     油门 → GP26 (ADC0)
#     离合 → GP27 (ADC1)
#   NAU7802 x1（刹车，称重传感器）：
#     SDA → GP4
#     SCL → GP5
#     VIN → VBUS (5V) 或 3.3V（视模块板而定）
#     GND → GND
#
# 依赖库（放入 /lib 目录）：
#   cedargrove_nau7802
#
# 轴映射：
#   X 轴 → 油门
#   Y 轴 → 刹车
#   Z 轴 → 离合
# ================================================

import board
import analogio
import digitalio
import usb_hid
import struct
import time
import busio
import busio as _busio
from cedargrove_nau7802 import NAU7802, ConversionRate


# ================================================
# 校准参数
# 首次使用请进入校准模式（上电时按住 GP15）
# 将串口输出的 min/max 值填入此处
# ================================================

THROTTLE_MIN  =  25606   # 油门完全释放时的 ADC 值
THROTTLE_MAX  = 45451   # 油门踩到底时的 ADC 值

CLUTCH_MIN    =  27142   # 离合完全释放时的 ADC 值
CLUTCH_MAX    = 45800   # 离合踩到底时的 ADC 值

BRAKE_MIN     =    1000  # 刹车空载（无压力）时的 NAU7802 值
BRAKE_MAX     = 1200000  # 刹车满载（踩到底）时的 NAU7802 值

# 两端死区比例，防止传感器漂移导致轴无法稳定到达 0% 或 100%
DEADZONE = 0.02  # 2%


# ================================================
# HID 设备初始化
# ================================================

pedal_device = None
for device in usb_hid.devices:
    if device.usage == 0x04 and device.usage_page == 0x01:
        pedal_device = device
        break

if pedal_device is None:
    raise RuntimeError("未找到踏板 HID 设备，请检查 boot.py 是否正确")

_report      = bytearray(6)
_last_report = bytearray(6)


# struct 改为有符号短整型 'h' 而不是无符号 'H'
def send_axes(x, y, z):
    struct.pack_into('<hhh', _report, 0, x, y, z)
    if _report != _last_report:
        pedal_device.send_report(_report)
        _last_report[:] = _report


# ================================================
# 工具函数
# ================================================

def clamp(value, lo, hi):
    return max(lo, min(hi, value))


# map_to_axis 输出范围改为 -32768 ~ 32767
def map_to_axis(raw, raw_min, raw_max, invert=False):
    span = raw_max - raw_min
    if span == 0:
        return -32768

    ratio = (raw - raw_min) / span
    ratio = clamp(ratio, 0.0, 1.0)

    if ratio < DEADZONE:
        ratio = 0.0
    elif ratio > 1.0 - DEADZONE:
        ratio = 1.0
    else:
        ratio = (ratio - DEADZONE) / (1.0 - 2 * DEADZONE)

    if invert:
        ratio = 1.0 - ratio

    return int(ratio * 65535) - 32768  # 映射到 -32768 ~ 32767


# ================================================
# 霍尔传感器初始化（ADC）
# ================================================

throttle_adc = analogio.AnalogIn(board.GP27)  # 油门
clutch_adc   = analogio.AnalogIn(board.GP26)  # 离合


# ================================================
# NAU7802 初始化（I²C，刹车）
# board.I2C() 默认使用 GP4(SDA) GP5(SCL)
# ================================================
i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
nau = NAU7802(i2c, address=0x2A, active_channels=1)

enabled = nau.enable(True)
if not enabled:
    raise RuntimeError("NAU7802 启动失败，请检查接线和供电")

# 80SPS：噪声与延迟的最佳平衡点，适合踏板场景
#nau.poll_rate = ConversionRate.RATE_40SPS
nau.poll_rate = 320

# 上电校准（执行时踏板须完全放开，不要施加任何压力）
nau.channel = 1
nau.calibrate("INTERNAL")
nau.calibrate("OFFSET")


def read_brake(samples=2):
    """
    多次采样取平均，提高读数稳定性
    每次等待数据就绪，超时 200ms 则返回 None
    """
    sample_sum = 0
    count = samples
    while count > 0:
        start = time.monotonic()
        while not nau.available():
            if time.monotonic() - start > 0.2:
                return None
        sample_sum += nau.read()
        count -= 1
    return int(sample_sum / samples)


# ================================================
# 校准模式
# 上电时按住 GP15 进入
# 需先在 boot.py 注释掉 usb_cdc.disable() 才能看到串口输出
# ================================================

cal_btn = digitalio.DigitalInOut(board.GP15)
cal_btn.direction = digitalio.Direction.INPUT
cal_btn.pull = digitalio.Pull.UP

if not cal_btn.value:
    print("=== 校准模式 ===")
    print("请将所有踏板完全放开，然后依次缓慢踩到底再松开")
    print("观察串口输出，记录每个传感器的 min 和 max 值")
    print("完成后将这些值填入 code.py 顶部的校准参数，然后重启")
    print("---")

    # 采初始值
    t_min = t_max = throttle_adc.value
    c_min = c_max = clutch_adc.value
    b_init = read_brake(samples=4)
    b_min  = b_max = b_init if b_init is not None else 0

    while True:
        t = throttle_adc.value
        c = clutch_adc.value
        b = read_brake(samples=2)

        t_min = min(t_min, t); t_max = max(t_max, t)
        c_min = min(c_min, c); c_max = max(c_max, c)
        if b is not None:
            b_min = min(b_min, b); b_max = max(b_max, b)

        print(
            f"油门 {t:6d} [{t_min:6d}~{t_max:6d}]  "
            f"离合 {c:6d} [{c_min:6d}~{c_max:6d}]  "
            f"刹车 {b} [{b_min}~{b_max}]"
        )
        time.sleep(0.1)


# ================================================
# 启动时发送归零报告
# ================================================

last_brake_raw = BRAKE_MIN
send_axes(-32768, -32768, -32768)  # 全部归零（踏板全部释放）


# ================================================
# 主循环
# ================================================

while True:

    # 油门（霍尔，ADC）
    throttle_raw  = throttle_adc.value
    throttle_axis = map_to_axis(throttle_raw, THROTTLE_MIN, THROTTLE_MAX, invert=True)

    # 离合（霍尔，ADC）
    clutch_raw  = clutch_adc.value
    clutch_axis = map_to_axis(clutch_raw, CLUTCH_MIN, CLUTCH_MAX, invert=True)

    # 刹车（NAU7802，称重传感器）
    brake_raw = read_brake(samples=2)
    if brake_raw is None:
        brake_raw = last_brake_raw   # 超时时保持上次值，不跳变
    else:
        last_brake_raw = brake_raw
    brake_axis = map_to_axis(brake_raw, BRAKE_MIN, BRAKE_MAX)

    # 发送 HID 报告：X=油门，Y=刹车，Z=离合
    send_axes(throttle_axis, brake_axis, clutch_axis)

    # ~1000Hz 轮询（实际受 NAU7802 采样率限制，约 320Hz）
    time.sleep(0.001)