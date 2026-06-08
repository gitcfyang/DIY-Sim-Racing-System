import usb_hid
import usb_cdc
import storage

# 调试阶段请注释掉以下两行，以便查看串口输出
#usb_cdc.disable()
#storage.disable_usb_drive()

# 踏板 HID 描述符
# 3个轴：X（油门）、Y（刹车）、Z（离合）
# 每轴 16bit 无符号，范围 0~65535
PEDAL_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,        # Usage Page (Generic Desktop)
    0x09, 0x04,        # Usage (Joystick)
    0xA1, 0x01,        # Collection (Application)
    0x85, 0x05,        #   Report ID (5)

    0x09, 0x30,        #   Usage (X)  → 油门
    0x09, 0x31,        #   Usage (Y)  → 刹车
    0x09, 0x32,        #   Usage (Z)  → 离合

    0x16, 0x00, 0x80,  #   Logical Minimum (-32768)
    0x26, 0xFF, 0x7F,  #   Logical Maximum (32767)
    0x75, 0x10,        #   Report Size (16 bit)
    0x95, 0x03,        #   Report Count (3)
    0x81, 0x02,        #   Input (Data, Variable, Absolute)

    0xC0,              # End Collection
))

pedals = usb_hid.Device(
    report_descriptor=PEDAL_REPORT_DESCRIPTOR,
    usage_page=0x01,
    usage=0x04,
    report_ids=(5,),
    in_report_lengths=(6,),   # 3轴 × 2字节 = 6字节
    out_report_lengths=(0,),
)

usb_hid.enable((pedals,))