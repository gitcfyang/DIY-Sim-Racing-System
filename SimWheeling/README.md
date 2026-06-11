# 🏎️ SimWheeling — DIY GT3 风格方向盘

> 一个功能完整的 GT3 风格赛车模拟器方向盘：碳纤维面板、3D 打印握把包翻毛皮、12 个按钮、5 个旋钮编码器、磁吸换挡拨片。  
> 外形设计参考**阿斯顿·马丁 Vantage GT3 赛车方向盘**，机械结构从零独立建模，电子系统为自主开发。  
> 主控：**树莓派 Pico（RP2040）** + **MCP23017** IO 扩展芯片，运行 **CircuitPython**。


---

## 📐 设计概览

本方向盘复刻了真实 GT3 赛车的操作布局：

| 特性 | 规格 |
|---|---|
| **按钮** | 12 个（MCP23017 I²C 扩展）+ 2 个直连（换挡拨片） |
| **旋钮编码器** | 5 个（MAP、TC、PRO、CAL、WIPER） |
| **前面板** | 碳纤维（可用铝合金替代） |
| **后面板** | 碳纤维 + 后部按钮护盖 |
| **握把** | 3D 打印 + 羽毛球手胶 包裹 |
| **换挡拨片** | 磁吸式（3D 打印底座 + 拨片臂） |
| **连接方式** | USB-C（RP2040 原生 USB HID） |

---

## 🗂️ 文件夹结构

```
SimWheeling/
├── CarbonfiberComponents/
│   ├── Drawing1.dwg                  ← 前面板切割图
│   ├── Drawing2.dwg                  ← 后面板切割图
│   ├── Drawing3.dwg                  ← 辅助板件
│   └── Drawing4.dwg                  ← 辅助板件
├── PrintedComponents/
│   ├── Grip Left Front x1.stl        ← 左握把（前半）
│   ├── Grip Left Rear x1.stl         ← 左握把（后半）
│   ├── Grip Right Front x1.stl       ← 右握把（前半）
│   ├── Grip Right Rear x1.stl        ← 右握把（后半）
│   ├── Hub Spacer x1.stl             ← 快拆转接垫圈
│   ├── Left Button Insert x1.stl     ← 左侧按钮嵌板
│   ├── Right Button Insert x1.stl    ← 右侧按钮嵌板
│   ├── Left Rear Button Cover x1.stl ← 左后按钮护盖
│   ├── Right Rear Button Cover x1.stl← 右后按钮护盖
│   ├── MCP23017Base x1.stl           ← MCP23017 扩展板安装座
│   ├── PicoBase x1.stl               ← RP2040 Pico 安装座
│   ├── Knob旋钮/
│   │   └── Rotary Encoder Knob x5.stl ← 编码器旋钮帽
│   └── Shifter换挡拨片/
│       ├── Base Bottom x2.stl        ← 拨片底座（下）
│       ├── Base Top x2.stl           ← 拨片底座（上）
│       ├── Lever x2.stl              ← 拨片臂
│       └── Shifter Spacer x2.stl     ← 拨片垫片
├── WheelCode/
│   ├── boot.py                         ← CircuitPython 启动文件
│   ├── code.py                         ← 主固件程序
│   ├── button_config.py                ← 按钮映射配置文件
│   └── lib/                            ← 依赖库
│       ├── adafruit_bus_device/        ← I²C/SPI 总线助手
│       └── adafruit_mcp230xx/          ← MCP23017 驱动
└── README.md                           ← 你在这里
```

---

## 🔌 电路架构

```
┌─────────────────────────────────────────────┐
│                   电脑 PC                     │
│         （模拟器识别为 USB HID 游戏手柄）       │
└──────────────────┬──────────────────────────┘
                   │ USB-C
┌──────────────────▼──────────────────────────┐
│          树莓派 Pico（RP2040）               │
│  - USB HID（摇杆 + 游戏手柄）                 │
│  - I²C 主机 → MCP23017                      │
│  - GPIO GP0 → 升档拨片（直连）                │
│  - GPIO GP1 → 降档拨片（直连）                │
│  - 5× 旋转编码器输入                         │
└──────────────────┬──────────────────────────┘
                   │ I²C（SDA / SCL）
┌──────────────────▼──────────────────────────┐
│           MCP23017（IO 扩展芯片）             │
│  GPA0~5 → 按钮 1-6（左侧）                    │
│  GPB0~5 → 按钮 7-12（右侧）                   │
└─────────────────────────────────────────────┘
```

---

## 🎮 按钮布局（GT3 风格）

### 左侧按钮（MCP23017 GPA0~5）

| 引脚 | 按钮编号 | 标签 | 功能 |
|---|---|---|---|
| GPA0 | 1 | **PTT** | 无线电 / 语音 |
| GPA1 | 2 | **OT** | 超车模式 |
| GPA2 | 3 | **MF↑** | 多功能菜单上 |
| GPA3 | 4 | **MF↓** | 多功能菜单下 |
| GPA4 | 5 | **PIT** | 进站限速 |
| GPA5 | 6 | **OK** | 菜单确认 |

### 右侧按钮（MCP23017 GPB0~5）

| 引脚 | 按钮编号 | 标签 | 功能 |
|---|---|---|---|
| GPB0 | 7 | **LIGHT** | 大灯 |
| GPB1 | 8 | **←** | 左转向灯 |
| GPB2 | 9 | **VIEW** | 视角/HUD 切换 |
| GPB3 | 10 | **→** | 右转向灯 |
| GPB4 | 11 | 自定义 | 可分配按钮 11 |
| GPB5 | 12 | 自定义 | 可分配按钮 12 |

### 换挡拨片（直连 GPIO）

| GPIO | 按钮编号 | 功能 |
|---|---|---|
| GP0 | 13 | ⬆️ 升档 |
| GP1 | 14 | ⬇️ 降档 |

### 旋钮编码器（直连 GPIO）

| 编码器 | 按钮编号 | 标签 | 功能 |
|---|---|---|---|
| 0 | 15, 16 | **MAP** | 引擎 map / 燃油混合比 |
| 1 | 17, 18 | **TC** | 牵引力控制 |
| 2 | 19, 20 | **PRO** | 动力输出 / 能量回收 |
| 3 | 21, 22 | **CAL** | 校准 / 设置 |
| 4 | 23, 24 | **WIPER** | 雨刷速度 |

> 合计 HID 报告：**32 个按钮事件**（12 个按钮 + 2 个拨片 + 5 个旋钮 × 2 方向）。电脑识别为标准 USB 游戏手柄，所有主流模拟器即插即用。


---

## 🔗 相关项目

- [🦶 SimPedal — 踏板制作教程](../SimPedal/README.md)
- [🏗️ SimBase — 基座制作教程](../SimBase/README.md)
- [📦 返回主 README](../README.md)
