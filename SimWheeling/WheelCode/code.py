# ================================================
# code.py
# GT3 模拟器方向盘主程序
#
# 硬件：
#   RP2040 (Raspberry Pi Pico)
#   MCP23017 x1（I²C，接12个按钮）
#   旋转编码器 x5（MAP/TC/PRO/CAL/WIPER）
#   直连按钮 x2（升档/降档拨片）
#
# 依赖库（放入 /lib 目录）：
#   adafruit_mcp230xx
#   adafruit_bus_device
# ================================================

import board
import busio
import digitalio
import rotaryio
import usb_hid
import struct
import time

from adafruit_mcp230xx.mcp23017 import MCP23017
from button_config import BUTTON_MAP, DIRECT_BUTTON_MAP, ENCODER_MAP, ENCODER_PULSE_MS


# ================================================
# HID 设备初始化
# ================================================

# 找到 boot.py 中注册的自定义手柄设备
gamepad_device = None
for device in usb_hid.devices:
    if device.usage == 0x05 and device.usage_page == 0x01:
        gamepad_device = device
        break

if gamepad_device is None:
    raise RuntimeError("未找到手柄 HID 设备，请检查 boot.py 是否正确")

# 32位按键状态，每一位对应一个按键（bit0=按键1，bit1=按键2...）
button_states = 0x00000000

# 记录上次发送的报告，避免重复发送（参考官方库设计）
_report      = bytearray(4)
_last_report = bytearray(4)


def press_button(btn_num):
    """按下指定按键（编号从1开始）"""
    global button_states
    button_states |= (1 << (btn_num - 1))
    _send_report()


def release_button(btn_num):
    """释放指定按键"""
    global button_states
    button_states &= ~(1 << (btn_num - 1))
    _send_report()


def pulse_button(btn_num, duration=ENCODER_PULSE_MS):
    """按下后立即释放，用于编码器触发"""
    press_button(btn_num)
    time.sleep(duration)
    release_button(btn_num)


def _send_report(always=False):
    """将当前按键状态发送给电脑
    only send if state changed，避免 USB 总线不必要的占用（参考官方库）"""
    struct.pack_into('<I', _report, 0, button_states)
    if always or _report != _last_report:
        # send_report 会自动处理 Report ID，不需要手动拼接
        gamepad_device.send_report(_report)
        _last_report[:] = _report

# ================================================
# MCP23017 初始化（I²C）
# ================================================

i2c = busio.I2C(scl=board.GP13, sda=board.GP12)
mcp = MCP23017(i2c, address=0x20)  # A0/A1/A2 全接 GND 时地址为 0x20

# 配置全部 16 个引脚为输入 + 内部上拉
# 未按下时为 High，按下后接 GND 变为 Low
mcp_pins = []
for i in range(16):
    pin = mcp.get_pin(i)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP
    mcp_pins.append(pin)


# ================================================
# 直连按钮初始化（升降档拨片）
# ================================================

upshift_pin = digitalio.DigitalInOut(board.GP0)
upshift_pin.direction = digitalio.Direction.INPUT
upshift_pin.pull = digitalio.Pull.UP

downshift_pin = digitalio.DigitalInOut(board.GP1)
downshift_pin.direction = digitalio.Direction.INPUT
downshift_pin.pull = digitalio.Pull.UP


# ================================================
# 编码器初始化
# ================================================

encoders = [
    rotaryio.IncrementalEncoder(board.GP3,  board.GP2),   # MAP
    rotaryio.IncrementalEncoder(board.GP4,  board.GP5),   # TC
    rotaryio.IncrementalEncoder(board.GP7,  board.GP6),   # PRO
    rotaryio.IncrementalEncoder(board.GP8,  board.GP9),   # CAL
    rotaryio.IncrementalEncoder(board.GP10, board.GP11),  # WIPER
]

# 记录每个编码器上一次的位置
last_encoder_positions = [enc.position for enc in encoders]


# ================================================
# 状态记录（用于边沿检测，避免重复触发）
# ================================================

last_mcp_states    = [pin.value for pin in mcp_pins]
last_upshift_state   = upshift_pin.value
last_downshift_state = downshift_pin.value


# ================================================
# 启动时发送全部释放状态（always=True 强制发送，参考官方库 reset_all）
# ================================================

_send_report(always=True)


# ================================================
# 主循环
# ================================================
while True:

    # ── MCP23017 按钮扫描 ──────────────────────────
    for pin_index, hid_btn in BUTTON_MAP.items():
        current = mcp_pins[pin_index].value  # True=未按，False=按下

        if current != last_mcp_states[pin_index]:
            if not current:
                # 下降沿：按下
                press_button(hid_btn)
            else:
                # 上升沿：释放
                release_button(hid_btn)
            last_mcp_states[pin_index] = current

    # ── 升档拨片 ────────────────────────────────────
    up_now = upshift_pin.value
    if up_now != last_upshift_state:
        btn = DIRECT_BUTTON_MAP["UPSHIFT"]
        if not up_now:
            press_button(btn)
        else:
            release_button(btn)
        last_upshift_state = up_now

    # ── 降档拨片 ────────────────────────────────────
    dn_now = downshift_pin.value
    if dn_now != last_downshift_state:
        btn = DIRECT_BUTTON_MAP["DOWNSHIFT"]
        if not dn_now:
            press_button(btn)
        else:
            release_button(btn)
        last_downshift_state = dn_now

    # ── 编码器扫描 ──────────────────────────────────
    for i, enc in enumerate(encoders):
        pos = enc.position
        delta = pos - last_encoder_positions[i]

        if delta != 0:
            cw_btn, ccw_btn = ENCODER_MAP[i]

            # 每格触发一次脉冲
            # delta 可能大于1（快速旋转），逐格触发
            steps = abs(delta)
            btn = cw_btn if delta > 0 else ccw_btn

            for _ in range(steps):
                pulse_button(btn)

            last_encoder_positions[i] = pos

    # 1ms 轮询，响应足够快且不占满 CPU
    time.sleep(0.001)