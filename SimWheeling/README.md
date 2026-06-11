# 🏎️ SimWheeling — DIY GT3 风格方向盘

> 一个功能完整的 GT3 风格赛车模拟器方向盘：碳纤维面板、3D 打印握把包翻毛皮、12 个按钮、5 个旋钮编码器、磁吸换挡拨片。  
> 主控：**树莓派 Pico（RP2040）** + **MCP23017** IO 扩展芯片，运行 **CircuitPython**。

![SimWheeling 渲染图](Render%203.png "GT3 方向盘渲染图")

---

## 📐 设计概览

本方向盘复刻了真实 GT3 赛车的操作布局：

| 特性 | 规格 |
|---|---|
| **按钮** | 12 个（MCP23017 I²C 扩展）+ 2 个直连（换挡拨片） |
| **旋钮编码器** | 5 个（MAP、TC、PRO、CAL、WIPER） |
| **前面板** | 碳纤维（可用铝合金替代） |
| **后面板** | 碳纤维 + 后部按钮护盖 |
| **握把** | 3D 打印 + 翻毛皮/Alcantara 包裹 |
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
├── Stickers/
│   ├── Turn GTE Sticker Sheet Size A4.ai         ← 贴纸设计（Illustrator 可编辑）
│   ├── Turn GTE Sticker Sheet Size A4-01.png     ← 贴纸预览图
│   ├── Turn GTE Sticker Sheet With Cut Lines Size A4-01.png ← 含切割线的打印版
│   └── Turn GTE Sticker Cutout Lines DXF.dxf     ← 切割机用切割线
├── Templates/
│   ├── Front Plate 1 to 1 Drawing A4 Paper.pdf   ← 前面板 1:1 打印模板
│   ├── Front Plate DXF_303.5mm Width.dxf         ← 前面板切割文件
│   ├── Rear Plate 1 to 1 scale A4 paper size.pdf ← 后面板 1:1 打印模板
│   ├── Rear Plate DXF_104.4mm Width.dxf          ← 后面板切割文件
│   ├── Left Grip Suede Template 1 to 1 scale A4 paper size.pdf  ← 左握把包皮模板
│   ├── Left Grip Suede Template DXF.dxf          ← 左握把包皮切割文件
│   ├── Right Grip Suede Template 1 to 1 scale A4 paper size.pdf ← 右握把包皮模板
│   └── Right Grip Suede Template DXF.dxf         ← 右握把包皮切割文件
├── WheelCode/
│   ├── boot.py                         ← CircuitPython 启动文件
│   ├── code.py                         ← 主固件程序
│   ├── button_config.py                ← 按钮映射配置文件
│   └── lib/                            ← 依赖库
│       ├── adafruit_bus_device/        ← I²C/SPI 总线助手
│       └── adafruit_mcp230xx/          ← MCP23017 驱动
├── Render 3.png                        ← 成品渲染图
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

## 🛠️ 制作步骤

### 第一步：采购电子元件

| 元件 | 数量 | 备注 |
|---|---|---|
| 树莓派 Pico（RP2040） | 1 | Pico W 也可以（WiFi 用不上） |
| MCP23017 I²C IO 扩展芯片 | 1 | DIP-28 直插或模块板均可 |
| 12mm 轻触按钮 | 12 | 自复位型，按需选择按压力度 |
| 旋转编码器（EC11 或同类） | 5 | 带按键可选（代码中未使用按键功能） |
| 微动开关（拨片用） | 2 | 超小型，如 D2HW-BR213MR |
| 磁铁（拨片用） | 4 | 小型钕磁铁，约 6×3mm |
| 导线（28-30 AWG） | 适量 | 按钮矩阵和 I²C 布线 |
| USB-C 数据线 | 1 | 连接 Pico 到电脑 |

### 第二步：3D 打印所有零件

打印 `PrintedComponents/` 中的以下文件：

| 零件 | 文件 | 数量 | 材料 | 备注 |
|---|---|---|---|---|
| 左握把前 | `Grip Left Front x1.stl` | 1 | PETG / ABS | 外露面——打磨光滑 |
| 左握把后 | `Grip Left Rear x1.stl` | 1 | PETG / ABS | 隐藏面 |
| 右握把前 | `Grip Right Front x1.stl` | 1 | PETG / ABS | 外露面——打磨光滑 |
| 右握把后 | `Grip Right Rear x1.stl` | 1 | PETG / ABS | 隐藏面 |
| 快拆垫圈 | `Hub Spacer x1.stl` | 1 | PLA / PETG | 快拆适配垫圈 |
| 左按钮嵌板 | `Left Button Insert x1.stl` | 1 | PLA | 固定左侧 6 个按钮 |
| 右按钮嵌板 | `Right Button Insert x1.stl` | 1 | PLA | 固定右侧 6 个按钮 |
| 左后按钮护盖 | `Left Rear Button Cover x1.stl` | 1 | PLA | 保护后部按钮 |
| 右后按钮护盖 | `Right Rear Button Cover x1.stl` | 1 | PLA | 保护后部按钮 |
| MCP23017 底座 | `MCP23017Base x1.stl` | 1 | PLA | IO 扩展板安装座 |
| Pico 底座 | `PicoBase x1.stl` | 1 | PLA | RP2040 安装座 |
| 旋钮帽 | `Knob旋钮/Rotary Encoder Knob x5.stl` | 5 | PLA | 编码器旋钮帽 |
| 拨片底座下 | `Shifter换挡拨片/Base Bottom x2.stl` | 2 | PETG | 拨片底座下半 |
| 拨片底座上 | `Shifter换挡拨片/Base Top x2.stl` | 2 | PETG | 拨片底座上半 |
| 拨片臂 | `Shifter换挡拨片/Lever x2.stl` | 2 | PETG/ABS | 拨片臂主体 |
| 拨片垫片 | `Shifter换挡拨片/Shifter Spacer x2.stl` | 2 | PLA | 拨片间隔垫片 |

> 🔑 **打印参数建议：** 层高 0.2mm，4 层外壳，结构件填充 40%。握把打印后打磨至 400 目以上，为包裹翻毛皮做准备。

### 第三步：加工碳纤维面板

将 `CarbonfiberComponents/` 中的 `Drawing1.dwg` ~ `Drawing4.dwg` 发给碳纤维加工商，或使用 `Templates/` 中的 DXF 文件：

| 板件 | 模板文件 | 宽度 | 建议厚度 |
|---|---|---|---|
| **前面板** | `Front Plate DXF_303.5mm Width.dxf` | 303.5mm | ~3mm 碳纤维板 |
| **后面板** | `Rear Plate DXF_104.4mm Width.dxf` | 104.4mm | ~2mm 碳纤维板 |

> 💡 **预算方案：** 用 3mm 铝合金甚至 3D 打印 PLA 代替碳纤维板。碳纤维看起来更高级，但结构上并非必须。

### 第四步：打印并粘贴按钮贴纸

使用 `Stickers/` 中的贴纸套件给按钮标注标签：

1. 用**不干胶乙烯基贴纸**或透明标签纸打印 `Turn GTE Sticker Sheet Size A4-01.png`
2. 如果你有刻字机（Cricut/Silhouette），用 `Turn GTE Sticker Cutout Lines DXF.dxf` 做精准切割
3. 可编辑的 `.ai` 文件（`Turn GTE Sticker Sheet Size A4.ai`）支持在 Illustrator 中自定义标签文字
4. 将贴纸粘贴到 3D 打印的 `Left Button Insert` 和 `Right Button Insert` 上

### 第五步：包裹翻毛皮握把

1. 按 1:1 比例打印握把模板：
   - `Templates/Left Grip Suede Template 1 to 1 scale A4 paper size.pdf`
   - `Templates/Right Grip Suede Template 1 to 1 scale A4 paper size.pdf`
2. 用模板在翻毛皮/Alcantara 布料上裁出精确形状（也可将 DXF 发给布料切割商）
3. 在握把表面和布料背面均匀涂上**接触型胶水**（如 3M Super 77）
4. 从内侧边缘开始，逐步向外包裹
5. 用锋利的笔刀修剪多余的布料
6. 用 DXF 文件可实现机器精准裁布

### 第六步：方向盘总装

#### 6a. 按钮和编码器安装
1. 将按钮和旋转编码器焊接到洞洞板或直接飞线
2. 将按钮装入 `Left Button Insert` 和 `Right Button Insert`
3. 将旋转编码器穿过前面板——将旋钮帽按到编码器轴上
4. 将 MCP23017 固定在 `MCP23017Base` 上，Pico 固定在 `PicoBase` 上

#### 6b. 接线
```
Pico GP4 (SDA) → MCP23017 SDA
Pico GP5 (SCL) → MCP23017 SCL
Pico 3V3(OUT)  → MCP23017 VDD
Pico GND       → MCP23017 VSS
Pico GP0       → 升档微动开关
Pico GP1       → 降档微动开关
Pico GP6~15    → 5× 旋转编码器（A/B 引脚）
```
- 所有 MCP23017 GPA/GPB 引脚 → 各轻触按钮
- 每个按钮按下时接通 GND（代码使用内部上拉电阻）

> 📐 **详细引脚分配请参考 `WheelCode/code.py` 和 `button_config.py`**，代码有详细注释，很容易重新映射。

#### 6c. 层叠组装
1. **前面板 → 按钮嵌板 → 按钮和编码器**
2. **Pico + MCP23017 电路板**安装在前面板后方的底座上
3. **后面板**将各层夹在一起
4. **左右握把**通过螺丝固定在两侧（夹在前后面板之间）
5. **快拆垫圈**居中安装——与 SimBase 的 70mm 快拆配合
6. **后部按钮护盖**保护背面的按钮

#### 6d. 磁吸拨片组装
1. 每组拨片由 `Base Bottom` + `Base Top` 上下夹合
2. 磁铁槽对面相吸放置（吸力产生清脆的啪嗒手感）
3. 用转轴螺丝安装 `Lever` 拨片臂——应有清脆的段落感
4. 将组装好的拨片单元安装到方向盘背面
5. 调整微动开关位置，使拨片在磁吸咬合点时刚好触发

### 第七步：烧录固件

1. 在树莓派 Pico 上安装 **CircuitPython**：
   - 按住 BOOTSEL 键插入 USB → 将 CircuitPython UF2 文件拖入出现的 RPI-RP2 驱动器
2. 将 `WheelCode/` 的全部内容复制到 `CIRCUITPY` 驱动器：
   ```
   CIRCUITPY/
   ├── boot.py
   ├── code.py
   ├── button_config.py
   └── lib/
       ├── adafruit_bus_device/
       └── adafruit_mcp230xx/
   ```
3. 方向盘应被电脑识别为 **USB HID 游戏手柄**
4. 用 `../SimBase/BaseSoftware/JoystickTest.exe` 测试所有按钮是否正常
5. 如需自定义按钮映射，直接编辑 `button_config.py`——修改后自动生效，无需重新编译

---

## 🎮 模拟器中的设置

方向盘被识别为游戏手柄后：

1. **轴分配**——方向盘本身没有转向轴（转向由 SimBase 提供），编码器脉冲以按钮形式输出
2. **按钮映射**——共 12 个面板按钮 + 2 个拨片 + 10 个编码器方向（合计 24 个有效按钮事件）
3. **编码器行为**——每格输出一个按钮脉冲；部分模拟器原生支持"编码器"模式，否则映射为"增加/减少"配对即可

### 推荐游戏内映射

| 控制 | 建议绑定 |
|---|---|
| MAP +/- | 引擎 map / 燃油混合 |
| TC +/- | 牵引力控制 |
| PRO +/- | 刹车平衡 / ABS |
| CAL +/- | 差速器 / 防倾杆 |
| WIPER +/- | 雨刷速度或音量 |

---

## 📺 效果参考

![Render](Render%203.png)

渲染图展示了完整装配的方向盘：碳纤维面板、包裹翻毛皮的握把、按钮标签和编码器旋钮。

---

## 🔗 相关项目

- [🦶 SimPedal — 踏板制作教程](../SimPedal/README.md)
- [🏗️ SimBase — 基座制作教程](../SimBase/README.md)
- [📦 返回主 README](../README.md)
