<div align="center">

# ZDEM Model Visualization Editor

**ZDEM 模型可视化编辑器 | ZDEM Model File Visualization Tool**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySide6](https://img.shields.io/badge/PySide-6.5%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

</div>

基于 PySide6 的 ZDEM 模型文件可视化与编辑工具，支持 WALL、GLINE、BOX 和 PROP P4 等多种对象类型的解析、渲染和交互操作。

> A PySide6-based graphical tool for visualizing and editing ZDEM model files. Supports parsing, rendering, and interactive manipulation of object types including WALL, GLINE, BOX, and PROP P4.

---

## 技术特性 | Features

| 中文特性 | English Feature | 说明 / Description |
|---------|----------------|-------------------|
| 多对象支持 | Multi-Object Support | 支持 WALL、GLINE、BOX、PROP P4 四种对象 |
| 交互式画布 | Interactive Canvas | 缩放、平移、选择高亮，鼠标和键盘快捷键 |
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

工具通过解析 ZDEM 模型定义文件，将文本描述的结构化对象数据转换为内存中的模型数据结构，然后利用 PySide6 的 QGraphicsView 框架进行可视化渲染。

核心解析流程：

1. **词法分析**：读取文件行，识别 BOX、WALL、GLINE、PROP P4 等关键字
2. **语法解析**：按对象类型规则提取坐标、颜色、参数
3. **模型构建**：将解析结果组装为 ZDEMModel 对象树
4. **渲染绘制**：在 QGraphicsScene 中绘制几何图形，支持交互操作

> The tool parses ZDEM model definition files, converting structured text into in-memory model data structures, then renders them using the PySide6 QGraphicsView framework.

---

## 模块文档 | Module Reference

| 模块 | 功能 |
|------|------|
| `zdem_editor/core/models.py` | 数据模型定义：Wall、GLine、Box、PropP4、ZDEMModel |
| `zdem_editor/core/parser.py` | 文件解析器：读取 .zdem 和 Python 脚本格式 |
| `zdem_editor/ui/canvas.py` | 交互式画布：缩放、平移、对象选择高亮 |
| `zdem_editor/ui/main_window.py` | 主窗口（中文界面） |
| `zdem_editor/ui/main_window_en.py` | 主窗口（英文界面） |
| `zdem_editor/utils/font_config.py` | 字体配置，跨平台兼容 |
| `zdem_editor/utils/helpers.py` | 工具函数：坐标提取、颜色标准化 |

---

## 快速开始 | Quick Start

```bash
# 克隆仓库
git clone https://github.com/Phoenix0531-sudo/ZDEM_Model_Visualization_Editor.git
cd ZDEM_Model_Visualization_Editor

# 安装依赖
pip install -r requirements.txt

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

工具在画布中以图形方式渲染模型对象，状态栏显示当前鼠标位置的坐标。对象类型及视觉表示如下：

| 对象类型 | 颜色 | 描述 |
|---------|------|------|
| BOX | 蓝色 | 矩形区域，定义模型几何边界 |
| GLINE | 绿色 | 几何线段，连接关键点 |
| WALL | 红色 | 墙体结构，物理边界 |
| PROP P4 | 自定义 | 四边形区域 |

> The tool renders model objects graphically on the canvas. The status bar displays real-time mouse coordinates.

---

## 安装与运行 | Installation

### 系统要求

- Python 3.8 或更高版本
- PySide6 6.5+
- Windows 7+ / Linux / macOS

### 依赖安装

```bash
pip install -r requirements.txt
```

### 运行

```bash
python main.py
```

或双击 `start.bat`（Windows）。

---

## Docker 使用 | Docker Usage

ZDEM Model Visualization Editor 是 PySide6 桌面 GUI 应用，Docker 环境主要用于**构建验证和依赖安装测试**，不适合作为主要的 GUI 运行方式。

> This tool is a PySide6 desktop GUI application. The Docker environment is intended for **build verification and dependency testing only** — it is not suitable for running the GUI.

```bash
# 构建镜像
docker build -t zdem-editor .

# 验证导入
docker run --rm zdem-editor python -c "from zdem_editor.core.models import ZDEMModel; print('Import OK')"
```

---

## 项目结构 | Project Structure

```
ZDEM_Model_Visualization_Editor/
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
    │   ├── canvas.py        # 交互式画布
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
  title = {ZDEM Model Visualization Editor},
  year = {2026},
  url = {https://github.com/Phoenix0531-sudo/ZDEM_Model_Visualization_Editor}
}
```

---

## 许可证 | License

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

> This project is open-sourced under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center"><strong>Made for the ZDEM and geotechnical modeling community</strong></div>
