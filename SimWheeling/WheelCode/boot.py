import usb_hid
import usb_cdc
import storage

#usb_cdc.disable()       # 禁用串口
#storage.disable_usb_drive()

# 自定义手柄描述符
# 支持 32 个按键，无轴，无 Hat switch
# 按键 1~24 实际使用，25~32 备用
GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,        # Usage Page (Generic Desktop)
    0x09, 0x05,        # Usage (Gamepad)
    0xA1, 0x01,        # Collection (Application)
    0x85, 0x04,        #   Report ID (4)

    # 按键区：32个按键
    0x05, 0x09,        #   Usage Page (Button)
    0x19, 0x01,        #   Usage Minimum (Button 1)
    0x29, 0x20,        #   Usage Maximum (Button 32)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0x01,        #   Logical Maximum (1)
    0x75, 0x01,        #   Report Size (1 bit)
    0x95, 0x20,        #   Report Count (32)
    0x81, 0x02,        #   Input (Data, Variable, Absolute)

    0xC0,              # End Collection
))

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,
    usage=0x05,
    report_ids=(4,),
    in_report_lengths=(4,),    # 32个按键 = 4字节，send_report 自动处理 Report ID
    out_report_lengths=(0,),
)

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     usb_hid.Device.CONSUMER_CONTROL,
     gamepad)
)