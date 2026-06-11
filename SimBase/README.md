# 🏗️ SimBase — DIY 直驱力反馈方向盘基座

> 基于 **ODrive 伺服驱动** + **伺服电机** 的直驱力反馈方向盘基座，搭载 **FFBeast Wheel** 开源固件。  
> 兼容标准 70mm PCD 快拆方向盘。

---

## 📐 设计理念

SimBase 的核心是一块 **ODrive 伺服驱动器** 搭配一颗高扭矩伺服电机，运行开源 [FFBeast Wheel](https://github.com/ffbeast-dev/ffbeast-wheel) 固件。这套组合带来：

- **直驱扭矩**——无皮带、无齿轮，零间隙、零延迟
- **开源力反馈**——通过 FFBeast Wheel UI 自由调节各种力反馈效果
- **标准快拆接口**——兼容市面上 70mm PCD 快拆方向盘
- **紧凑 3D 打印外壳**——防尘整洁

---

## 🗂️ 文件夹结构

```
SimBase/
├── BaseSoftware/
│   ├── ffbeast-wheel-hex/              ← 预编译 ODrive 固件 (.hex)
│   ├── ffbeast-wheel-api-lib/          ← C++ 方向盘 API 库 (hidapi)
│   ├── ffbeast-wheel-api-example-app/  ← 基于 API 的 Qt 示例应用
│   ├── ffbeast-wheel-ui/               ← FFBeast Wheel 配置工具 (Qt6)
│   │   ├── ffbeast-wheel-setup-RC.24.1.5.exe  ← 安装包
│   │   ├── wheel_effects_profiles/     ← 力反馈效果预设
│   │   └── wheel_periphery_profiles/   ← 外设/按钮映射预设
│   ├── JoystickTest.exe                ← 通用摇杆测试工具
│   └── VKB_JoyTester.exe / .ini        ← VKB 摇杆诊断工具
├── MetalComponents/                    ← 金属零件（待添加 DXF/STEP）
├── PrintedComponents/
│   └── Shell x1.stl                    ← 外壳主体（3D 打印）
├── New Text Document (2).txt           ← 接线参考笔记
└── README.md                           ← 你在这里
```

---

## 🧰 核心部件

### 电子部分

| 部件 | 型号/规格 | 用途 |
|---|---|---|
| **伺服电机** | 高扭矩交流伺服（见 BOM） | 动力核心——直接输出力反馈扭矩到转向轴 |
| **电机驱动器** | ODrive v3.6（或 MksODriveMini） | 对伺服电机进行磁场定向控制（FOC） |
| **电源** | 24-48V DC，300W 以上 | 给 ODrive + 电机供电 |
| **编码器** | 伺服电机内置 | 电机位置反馈，FOC 必需 |
| **USB 接口** | ODrive 原生 USB | 连接 PC 传输力反馈信号 |

### 机械部分

| 零件 | 材质 | 备注 |
|---|---|---|
| **MotorFrame（电机支架）** | 3D 打印 / 金属 | 固定伺服电机 |
| **Base Bottom（底座底板）** | 金属（见 Complete Assembly） | 刚性底板——固定在模拟器支架上 |
| **Base Top（底座顶板）** | 金属 | 顶部轴承支撑 |
| **Shell（外壳）** | 3D 打印（PLA/PETG） | 保护外罩 |
| **Quick Release（快拆）** | 70mm PCD QR 转接座 | 标准赛车快拆 |
| **Hub Plate + Spacer（转接盘+垫片）** | 金属 | 电机轴 → 快拆转接 |

---

## ⚡ 接线参考

参考 `New Text Document (2).txt` 中的笔记：

### 动力线（电机三相）
| 线色 | 接法 |
|---|---|
| 🔴 红色 | A 相 |
| 🔵 蓝色 | B 相 |
| 🟡 黄色 | C 相 |

### 编码器信号线
| 线色 | 接法 |
|---|---|
| 🔴 红色 | VCC（+5V） |
| ⚫ 黑色 | GND |
| 🟢 绿色 | A（正交信号） |
| 🟠 橙色 | B（正交信号） |
| 🟡 黄色 | Z（索引信号） |

> ⚠️ **务必对照你的电机说明书！** 不同厂家的线色可能不同。相线接错可能导致电机失控震荡——首次测试时务必先设置较低的电流限制。

---

## 🛠️ 制作步骤

### 第一步：采购核心部件

#### 物料清单（BOM）

| 物料 | 建议来源 | 备注 |
|---|---|---|
| 伺服电机（如 80ST-M02430 或类似） | 淘宝 / 1688 | 约 200-300W，3000 RPM，带编码器 |
| ODrive v3.6 主板 | [ODrive Robotics](https://odriverobotics.com/) | 或淘宝搜 MksODriveMini |
| 24-48V 直流电源（≥300W） | 淘宝 | 推荐 Mean Well LRS-350-48 |
| 70mm PCD 快拆 | 淘宝 | 通用模拟赛车快拆 |
| 轴承（电机轴支撑） | 淘宝 / 本地五金 | 参考 Complete Assembly 中的规格 |
| M3 / M4 / M5 螺丝 | 本地五金店 | 内六角、螺母、垫圈适量 |

### 第二步：3D 打印外壳

- 文件：`PrintedComponents/Shell x1.stl`
- 材料：**推荐 PETG**（耐热性优于 PLA，电机发热时不会软化）
- 填充率：20-30%
- 如果打印机尺寸不够，可能需要分体打印后拼接

### 第三步：加工金属零件

参考 [Complete Assembly](../Complete%20Assembly/) 文件夹中的以下文件：

- `Base Bottom.CATPart` — 底座安装板
- `Base Top.CATPart` — 顶部轴承/电机支撑
- `MotorFrame.CATPart` — 电机支架
- `Hub Plate.CATPart` + `Hub Spacer.CATPart` — 轴→快拆转接
- `QuickRelease.CATPart` — 快拆主体
- `HeatSink.CATPart` — ODrive 散热片

> 📝 导出为 `.DXF` 或 `.STEP` 格式发给激光切割或 CNC 加工。具体材质规格在 CATIA 文件中有记录。

### 第四步：机械装配

1. **将电机安装**到电机支架上 → 固定到底座底板
2. **安装轴承**到底座顶板，与电机轴对齐
3. **安装转接盘和垫片**到电机轴上
4. **安装快拆**到转接盘上
5. **连接底座顶板和底板**用立柱/侧板固定
6. 将电机三相线和编码器信号线接到 ODrive（参考上方接线说明）

### 第五步：烧录 ODrive 固件

1. 下载并安装 **FFBeast Wheel Setup**：
   - 运行 `BaseSoftware/ffbeast-wheel-ui/ffbeast-wheel-setup-RC.24.1.5.exe`
   - 安装包同时包含配置界面和固件烧录工具

2. 用 USB 线将 ODrive 连接到电脑

3. 烧录 FFBeast 固件：
   - 固件文件路径：`BaseSoftware/ffbeast-wheel-hex/ffbeast-wheel-odrive-RC.24.1.5.hex`
   - 使用 `odrivetool` 命令行工具或 FFBeast 设置向导进行烧录

4. 通过 FFBeast Wheel UI 运行电机校准：
   - 设置电机极对数、编码器 CPR、电流限制
   - 运行自动电机/编码器校准流程

### 第六步：配置力反馈

1. 启动 `ffbeast-wheel-ui`（Qt6 应用）
2. 配置以下内容：
   - **力反馈效果配置文件**——FFB 强度、阻尼、惯性、摩擦力
   - **外设配置文件**——按钮映射（如果方向盘通过基座连接）
3. 用 `JoystickTest.exe` 或 `VKB_JoyTester.exe` 测试输出是否正常
4. 在你喜欢的模拟器（iRacing、Assetto Corsa、ACC 等）中精细调节效果

### 第七步：安装外壳

- 将 3D 打印的 `Shell` 套在组装好的基座上
- 用 M3 螺丝固定（检查设计中的安装孔位）

---

## 🔧 软件速查表

| 工具 | 路径 | 用途 |
|---|---|---|
| **FFBeast Wheel UI** | `BaseSoftware/ffbeast-wheel-ui/` | 主配置和力反馈调节界面 |
| **API 库** | `BaseSoftware/ffbeast-wheel-api-lib/` | 用于开发自定义力反馈应用的 C++/Qt 库 |
| **示例应用** | `BaseSoftware/ffbeast-wheel-api-example-app/` | 演示如何使用 API 的 Qt 项目 |
| **ODrive 固件** | `BaseSoftware/ffbeast-wheel-hex/` | 预编译的 ODrive 固件 |
| **摇杆测试** | `BaseSoftware/JoystickTest.exe` | 验证轴和按钮输出 |
| **VKB 测试** | `BaseSoftware/VKB_JoyTester.exe` | 高级摇杆诊断工具 |

---

## ⚠️ 安全注意事项

- **高扭矩危险！** 直驱基座可产生 10+ Nm 的扭矩——运行时手指远离旋转部件
- **紧急停止：** 建议配置急停开关，或确保电源插座伸手可及
- **电流限制：** ODrive 配置中务必从低电流开始，逐步上调
- **散热：** 电机和 ODrive 在持续负载下会发热——确保散热片通风良好

---

## 🙏 致谢与参考

### 开源项目

| 项目 | 用途 | 修改说明 |
|---|---|---|
| [FFBeast Wheel](https://github.com/ffbeast-dev/ffbeast-wheel) | 力反馈固件及配置工具 | 原样使用其 ODrive 固件（`.hex`）和 Qt6 配置工具；轮边外设配置根据 SimWheeling 方向盘做了适配调整 |
| [ODrive](https://github.com/odriverobotics/ODrive) | 伺服电机 FOC 驱动平台 | 使用其硬件（v3.6）和基础驱动架构，FFBeast 在其上构建 FFB 协议层 |
| [HIDAPI](https://github.com/libusb/hidapi) | USB HID 通信库 | FFBeast API 库依赖，原样使用 |

### 说明

SimBase 的机械结构（电机支架、底座、快拆转接等）为本项目原创设计，参照 Complete Assembly 中的 CATIA 模型。

---

## 🔗 相关项目

- [🦶 SimPedal — 踏板制作教程](../SimPedal/README.md)
- [🏎️ SimWheeling — 方向盘制作教程](../SimWheeling/README.md)
- [📦 返回主 README](../README.md)
