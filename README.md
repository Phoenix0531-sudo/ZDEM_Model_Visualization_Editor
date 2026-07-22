<div align="center">

# ZDEM Model Editor

**tkinter + matplotlib editor for ZDEM model files**

[English](README.md) | [中文](README.zh-CN.md)

![CI](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor/actions/workflows/ci.yml/badge.svg)

**ZDEM 模型可视化编辑器 | ZDEM Model File Visualization Tool**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-8.5%2B-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.0%2B-orange)
![NumPy](https://img.shields.io/badge/NumPy-1.20%2B-lightblue)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

</div>

基于 tkinter 和 matplotlib 的 ZDEM 模型文件可视化与编辑工具，支持 WALL、GLINE、BOX 和 PROP P4 等多种对象类型的解析、渲染和交互操作。

> A tkinter + matplotlib-based tool for visualizing and editing ZDEM model files. Supports parsing, rendering, and interactive manipulation of object types including WALL, GLINE, BOX, and PROP P4.

---

## 技术特性 | Features

| 中文特性 | English Feature | 说明 / Description |
|---------|----------------|-------------------|
| 多对象支持 | Multi-Object Support | 支持 WALL、GLINE、BOX、PROP P4 四种对象 |
| 交互式画布 | Interactive Canvas | 使用 matplotlib FigureCanvasTkAgg 实现缩放、平移、选择 |
| 异步加载 | Async Loading | 大文件后台加载，界面保持响应 |
| 坐标系统 | Coordinate System | 第一象限坐标系，实时坐标显示 |
| 性能优化 | Performance | LOD 渲染、视口裁剪、智能缓存 |
| 对象选择 | Object Selection | 点击高亮、多选支持、Esc 取消选择 |
| 文件格式 | File Format Support | 解析 .zdem 文件及 Python 脚本格式的模型定义 |

---

## 目录 | Table of Contents

- [数据准备 | Data Preparation](#数据准备--data-preparation)
- [核心原理 | Core Method](#核心原理--core-method)
- [模块文档 | Module Reference](#模块文档--module-reference)
- [快速开始 | Quick Start](#快速开始--quick-start)
- [输出说明 | Output](#输出说明--output)
- [安装与运行 | Installation](#安装与运行--installation)
- [Docker 使用 | Docker Usage](#docker-使用--docker-usage)
- [项目结构 | Project Structure](#项目结构--project-structure)
- [引用 | Citation](#引用--citation)
- [许可证 | License](#许可证--license)

---

## 数据准备 | Data Preparation

本工具需要 ZDEM 格式的模型文件作为输入。支持的输入格式包括：

- **.zdem 文件**：标准 ZDEM 模型定义文件（如 `sample.zdem`）
- **Python 脚本**：包含 WALL/GLINE 等对象定义的 Python 文件（如 `Test/gen0.py`）

> This tool requires ZDEM-format model files as input. Supported formats include .zdem standard definition files and Python script files containing object definitions.

---

## 核心原理 | Core Method

工具通过解析 ZDEM 模型定义文件，将文本描述的结构化对象数据转换为内存中的模型数据结构，然后利用 matplotlib 的 FigureCanvasTkAgg 嵌入 tkinter 窗口进行可视化渲染。

核心解析流程：

1. **词法分析**：读取文件行，识别 BOX、WALL、GLINE、PROP P4 等关键字
2. **语法解析**：按对象类型规则提取坐标、颜色、参数
3. **模型构建**：将解析结果组装为 ZDEMModel 对象树
4. **渲染绘制**：在 matplotlib axes 中绘制几何图形，支持交互操作

> The tool parses ZDEM model definition files, converting structured text into in-memory model data structures, then renders them using matplotlib's FigureCanvasTkAgg embedded in a tkinter window.

---

## 模块文档 | Module Reference

| 模块 | 功能 |
|------|------|
| `zdem_editor/core/models.py` | 数据模型定义：Wall、GLine、Box、PropP4、ZDEMModel |
| `zdem_editor/core/parser.py` | 文件解析器：读取 .zdem 和 Python 脚本格式 |
| `zdem_editor/ui/canvas.py` | 基于 matplotlib 的交互式画布，缩放、平移、对象选择高亮 |
| `zdem_editor/ui/main_window.py` | 主窗口（中文界面），基于 tkinter |
| `zdem_editor/ui/main_window_en.py` | 主窗口（英文界面），基于 tkinter |
| `zdem_editor/utils/font_config.py` | 字体配置，跨平台兼容 |
| `zdem_editor/utils/helpers.py` | 工具函数：坐标提取、颜色标准化 |

---

## 快速开始 | Quick Start

```bash
# 克隆仓库
git clone https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor.git
cd ZDEM_Model_Editor

# 安装依赖（tkinter 为系统自带，无需 pip 安装）
pip install matplotlib numpy

# 启动应用
python main.py
```

启动后按 Ctrl+O 打开一个 .zdem 或 Python 脚本文件，程序将自动解析并显示模型。

### 快捷键

| 操作 | 快捷键 |
|------|--------|
| 打开文件 | Ctrl+O |
| 保存文件 | Ctrl+S |
| 退出程序 | Ctrl+Q |
| 缩放 | 鼠标滚轮 |
| 重置视图 | R |
| 适应视图 | F |
| 全选对象 | Ctrl+A |
| 清除选择 | Escape |

---

## 输出说明 | Output

工具在 matplotlib 画布中以图形方式渲染模型对象，状态栏显示当前鼠标位置的坐标。对象类型及视觉表示如下：

| 对象类型 | 颜色 | 描述 |
|---------|------|------|
| BOX | 蓝色 | 矩形区域，定义模型几何边界 |
| GLINE | 绿色 | 几何线段，连接关键点 |
| WALL | 红色 | 墙体结构，物理边界 |
| PROP P4 | 自定义 | 四边形区域 |

> The tool renders model objects graphically on the matplotlib canvas. The status bar displays real-time mouse coordinates.

---

## 安装与运行 | Installation

### 系统要求

- Python 3.8 或更高版本
- tkinter（通常随 Python 一起安装，Linux 下可能需要 `apt install python3-tk`）
- matplotlib 3.0+
- numpy 1.20+
- Windows 7+ / Linux / macOS

### 依赖安装

```bash
# matplotlib 和 numpy 通过 pip 安装
pip install -r requirements.txt

# Linux 用户需要额外安装 tkinter
# sudo apt install python3-tk
```

### 运行

```bash
python main.py
```

或双击 `start.bat`（Windows）。

---

## Docker 使用 | Docker Usage

ZDEM Model Editor 是 tkinter 桌面 GUI 应用，Docker 环境主要用于**构建验证和依赖安装测试**，不适合作为主要的 GUI 运行方式。tkinter 在 Docker 中需要 `tk-dev` 系统库支持，且需要 X11 转发才能显示窗口。

> This tool is a tkinter desktop GUI application. The Docker environment is intended for **build verification and dependency testing only** — it is not suitable for running the GUI. tkinter requires X11 forwarding in Docker for actual display.

```bash
# 构建镜像
docker build -t zdem-editor .

# 导入验证（非交互模式）
docker run --rm zdem-editor
```

---

## 项目结构 | Project Structure

```
ZDEM_Model_Editor/
├── main.py                  # 应用入口
├── start.bat                # Windows 启动脚本
├── requirements.txt         # Python 依赖
├── Dockerfile               # Docker 构建文件
├── LICENSE                  # MIT 许可证
├── .gitignore               # Git 忽略规则
├── .editorconfig            # 编辑器配置
├── CHANGELOG.md             # 变更日志
├── README.md                # 项目说明
├── docs/
│   └── index.md             # GitHub Pages 入口
├── Test/                    # 测试数据与测试脚本
│   ├── gen0.py
│   ├── shear0.py
│   ├── shear1.py
│   ├── test_enhanced_parser.py
│   └── test_prop_p4.py
└── zdem_editor/             # 主包
    ├── __init__.py
    ├── core/
    │   ├── models.py        # 数据模型
    │   └── parser.py        # 文件解析器
    ├── ui/
    │   ├── canvas.py        # matplotlib 交互式画布
    │   ├── main_window.py   # 主窗口（中文）
    │   └── main_window_en.py# 主窗口（英文）
    └── utils/
        ├── font_config.py   # 字体配置
        └── helpers.py       # 工具函数
```

---

## 引用 | Citation

```bibtex
@software{zdem_editor2026,
  title = {ZDEM Model Editor},
  year = {2026},
  url = {https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor}
}
```

---

## ZDEM Tool Family

Related open-source tools in the same ZDEM / DEM workflow (same author):

| Repo | Role |
|------|------|
| [ZDEM_ParticleTracker](https://github.com/Phoenix0531-sudo/ZDEM_ParticleTracker) | VisPy particle tracking desktop app (true-radius discs, permanent IDs) |
| [ZDEM_Archiver](https://github.com/Phoenix0531-sudo/ZDEM_Archiver) | Safe purge of timestep dumps while keeping reproducible sources |
| [ZDEM_Area_Conservation](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation) | Delaunay coverage area vs load step |
| [ZDEM_Bond_Fracture](https://github.com/Phoenix0531-sudo/ZDEM_Bond_Fracture) | Bond damage / fracture time series + ROI |
| [ZDEM_Damage_Thresholds](https://github.com/Phoenix0531-sudo/ZDEM_Damage_Thresholds) | Damage evolution and crack thresholds |
| [ZDEM_DFN](https://github.com/Phoenix0531-sudo/ZDEM_DFN) | Discrete fracture network generation |
| [ZDEM_Model_Editor](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor) | tkinter + matplotlib model file editor |
| [ZDEM_Salt_Kinematics](https://github.com/Phoenix0531-sudo/ZDEM_Salt_Kinematics) | Salt kinematics automation for ZDEM outputs |
| [ZDEM3D_WEB](https://github.com/Phoenix0531-sudo/ZDEM3D_WEB) | 3D web CAE front (VTK + Django/React) |

Typical pipeline: **Model_Editor / DFN → ZDEM run → Archiver (disk) → ParticleTracker / Bond / Area / Salt / Damage (analysis)**.

## 许可证 | License

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

> This project is open-sourced under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center"><strong>Made for the ZDEM and geotechnical modeling community</strong></div>

## License

[MIT](LICENSE) — free for commercial use with attribution.
