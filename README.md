# DIY 赛车模拟器 — 完整方案

> 从零打造一套完整的 DIY 赛车模拟器：踏板、直驱力反馈基座、GT3 方向盘。  
> 以最低成本实现高品质模拟赛车体验。

---

## 项目概览

本项目包含三个独立但又可组合使用的 DIY 部件：

| 部件 | 说明 | 教程 |
|---|---|---|
| **SimPedal（脚踏板）** | 支持霍尔传感器与压力传感器的可互换式踏板组，可自由组合油门、刹车、离合。 | [📖 SimPedal 制作教程](SimPedal/README.md) |
| **SimBase（方向盘基座）** | 基于 ODrive 驱动 + 伺服电机的直驱力反馈基座，搭载 FFBeast 开源固件。 | [📖 SimBase 制作教程](SimBase/README.md) |
| **SimWheeling（方向盘）** | GT3 风格方向盘，RP2040 + MCP23017 方案，12 个按钮、5 个旋钮编码器、碳纤维面板、磁吸换挡拨片。 | [📖 SimWheeling 制作教程](SimWheeling/README.md) |

另外，[Complete Assembly](Complete%20Assembly/) 文件夹包含了完整的 CATIA 装配体及所有零件参考文件。

---

## 快速导航

- 🦶 **[制作踏板 →](SimPedal/README.md)**
- 🏗️ **[制作基座 →](SimBase/README.md)**
- 🏎️ **[制作方向盘 →](SimWheeling/README.md)**

---

## 文件类型说明

| 扩展名 | 用途 |
|---|---|
| `.STL` | 3D 打印模型文件 |
| `.DXF` | 激光/水刀切割图纸 |
| `.STEP` | CNC 加工用 CAD 交换格式 |
| `.CATPart` / `.CATProduct` | CATIA 原生 CAD 文件 |
| `.DWG` | AutoCAD 工程图（碳纤维板） |
| `.py` | CircuitPython 固件（RP2040） |
| `.pdf` | 折弯说明 / 1:1 模板 |
| `.ai` | Adobe Illustrator 文件（贴纸设计） |
| `.png` | 渲染参考图和贴纸预览 |

---

## 硬件方案概览

- **踏板**：Arduino 32u4（Pro Micro / Leonardo）+ 霍尔传感器 + HX711 压力传感器放大器
- **基座**：ODrive 伺服驱动器 + 伺服电机，运行 FFBeast 力反馈固件
- **方向盘**：树莓派 Pico（RP2040）+ MCP23017 IO 扩展芯片，运行 CircuitPython

---

## 致谢

踏板原始设计来自 **CNCDan**。方向盘与基座在此基础上扩展适配，构成本套完整方案。

## 许可证

本项目为开源 DIY 方案。欢迎自制、改进、分享！🏁
