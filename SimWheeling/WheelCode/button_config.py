# ================================================
# button_config.py
# 按钮映射配置文件
# 使用 MCP23017 GPA0~5 + GPB0~5，共12个按钮
# ================================================

BUTTON_MAP = {
    # GPA 组：GPA0~GPA5，共6个
    0:  1,   # GPA0 → PTT 无线电
    1:  2,   # GPA1 → OT  超车模式
    2:  3,   # GPA2 → MF↑ 菜单上
    3:  4,   # GPA3 → MF↓ 菜单下
    4:  5,   # GPA4 → PIT 进站限速
    5:  6,   # GPA5 → OK  菜单确认

    # GPB 组：GPB0~GPB5，共6个
    8:  7,   # GPB0 → LIGHT 大灯
    9:  8,   # GPB1 → 左转向灯
    10: 9,   # GPB2 → 视角/HUD 切换
    11: 10,  # GPB3 → 右转向灯
    12: 11,  # GPB4 → 按钮11
    13: 12,  # GPB5 → 按钮12
}

# 直连按钮：升降档拨片（编号接在MCP按钮之后）
DIRECT_BUTTON_MAP = {
    "UPSHIFT":   13,  # GP0
    "DOWNSHIFT": 14,  # GP1
}

# 编码器映射（编号继续顺延）
ENCODER_MAP = {
    0: (15, 16),  # MAP   增 / 减
    1: (17, 18),  # TC    增 / 减
    2: (19, 20),  # PRO   增 / 减
    3: (21, 22),  # CAL   增 / 减
    4: (23, 24),  # WIPER 增 / 减
}

ENCODER_PULSE_MS = 0.02