# ZDEM Model Visualization Editor

> 一个用于可视化和编辑 ZDEM 模型文件的高性能图形化工具

## 🚀 快速使用

### 方法1：直接运行
```bash
python main.py
```

### 方法2：使用启动脚本
双击 `start.bat` 文件

### 使用步骤
1. 启动程序后，点击"打开文件"按钮
2. 选择 `gen.py` 或 `shear.py` 文件
3. 程序会自动解析并显示模型
4. 在左侧面板查看对象信息和列表
5. **新功能**：点击对象列表中的对象可高亮显示对应线条
6. 按 `Esc` 键或菜单"视图→清除选择"来取消高亮

## ✅ 测试结果
- ✅ gen.py: 成功解析 2个WALL + 6个GLINE = 8个对象
- ✅ shear.py: 成功解析 1个WALL + 4个GLINE = 5个对象
- ✅ shear1.py: 成功解析 1个WALL + 3个PROP P4 = 4个对象
- ✅ 字体问题已解决：程序启动无警告信息
- ✅ 对象选择高亮功能完全正常
- ✅ WALL语法解析：支持标准格式和现有格式
- ✅ PROP P4四边形：支持四边形区域定义和可视化

## 🧪 测试文件
项目包含完整的测试套件，位于 `Test/` 文件夹中：

- **Test/test_selection.py** - 测试对象选择和高亮功能
- **Test/test_wall_syntax.py** - 测试WALL语法解析功能
- **Test/test_enhanced_parser.py** - 测试增强解析器鲁棒性
- **Test/test_prop_p4.py** - 测试PROP P4四边形功能
- **Test/gen0.py** - 测试数据文件（P1/P2格式）
- **Test/shear0.py** - 测试数据文件（混合格式）
- **Test/shear1.py** - 测试数据文件（复杂格式，含P4）

运行测试：
```bash
python Test\test_selection.py
python Test\test_wall_syntax.py
python Test\test_enhanced_parser.py
python Test\test_prop_p4.py
```

## 🔧 技术优化
- **字体配置**：自动配置系统字体，避免中文字体警告
- **英文界面**：主界面使用英文，确保跨平台兼容性
- **警告过滤**：智能过滤matplotlib字体警告
- **性能优化**：减少不必要的字体渲染开销
- **数据结构优化**：修复unhashable type错误，使用列表存储选中对象
- **解析器增强**：支持P1/P2格式、数字颜色、特殊颜色缩写等新语法

## 🐛 已修复的问题
- ✅ **unhashable type wall错误**：将选中对象存储从set改为list
- ✅ **字体警告问题**：完全消除matplotlib和tkinter字体警告
- ✅ **跨平台兼容性**：英文界面确保在不同系统上正常显示

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.5+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 核心特性

| 特性           | 描述                         |
| -------------- | ---------------------------- |
| 🚀 **异步加载** | 大文件后台加载，界面不卡顿   |
| 📐 **坐标系统** | 第一象限坐标系，实时坐标显示 |
| 🔬 **实验区域** | BOX区域管理，边界检测        |
| ⚡ **高性能**   | LOD渲染，视口裁剪，智能缓存  |
| 🎨 **交互编辑** | 拖拽操作，多选支持           |

## 🚀 快速开始

### 一键启动

### 三步上手
1. **启动程序** → 运行 `python main.py`
2. **加载文件** → 按 `Ctrl+O` 选择 `sample.zdem`
3. **开始使用** → 鼠标操作视图，点击选择对象


## 📁 文件支持

| 文件            | 类型       | 对象数 | 说明                       |
| --------------- | ---------- | ------ | -------------------------- |
| `sample.zdem`   | 标准格式   | 21个   | 完整示例，包含所有对象类型 |
| `Test/gen.py`   | Python脚本 | 9个    | 走滑实验，复杂几何结构     |
| `Test/shear.py` | Python脚本 | 2个    | 剪切实验，简单测试用例     |

## 🎨 对象类型

| 对象      | 颜色   | 描述     | 用途         |
| --------- | ------ | -------- | ------------ |
| **BOX**   | 🔵 蓝色 | 矩形区域 | 定义几何边界 |
| **GLINE** | 🟢 绿色 | 几何线段 | 连接关键点   |
| **WALL**  | 🔴 红色 | 墙体结构 | 物理边界     |

## ⌨️ 常用快捷键

### 文件操作
- `Ctrl+O` 打开文件
- `Ctrl+S` 保存文件
- `Ctrl+Q` 退出程序

### 视图控制
- `鼠标滚轮` 缩放视图
- `R` 重置视图
- `F` 适应视图
- `Ctrl+G` 切换坐标系

### 编辑操作
- `Ctrl+A` 全选对象
- `Escape` 清除选择
- `拖拽` 移动对象

> 📖 **完整快捷键**: 查看 [用户指南](docs/USER_GUIDE.md#快捷键参考)

## 🔬 实验区域

**BOX实验区域**是定义模型有效工作范围的核心概念：

- 🎯 **边界定义**: 设置模型的有效工作区域
- 🔍 **边界检查**: 自动检测对象是否在区域内
- 🎨 **可视化**: 半透明边框显示区域范围
- ⚙️ **灵活配置**: 自定义大小、颜色、显示状态

**使用方法**: `菜单 → 实验区域 → 配置实验区域`

## 📊 技术特性

### 🎯 坐标系统
- **第一象限**: 原点(0,0)左下角，Y轴向上
- **实时显示**: 鼠标坐标实时显示在状态栏
- **网格对齐**: 主网格1000单位，次网格200单位
- **精确定位**: 支持小数点后多位精度

### ⚡ 性能优化
- **异步加载**: 大文件后台处理，界面保持响应
- **LOD渲染**: 智能细节调整，提升渲染效率
- **视口裁剪**: 只绘制可见区域，节省资源
- **智能缓存**: 减少重复计算，提高性能

## 📖 文档

| 文档                            | 内容           | 适用对象 |
| ------------------------------- | -------------- | -------- |
| [快速开始](docs/QUICK_START.md) | 一分钟上手指南 | 新用户   |
| [功能特性](docs/FEATURES.md)    | 完整功能列表   | 了解功能 |
| [用户指南](docs/USER_GUIDE.md)  | 详细使用说明   | 深度使用 |

## 🛠️ 安装与运行

### 系统要求
- Python 3.8+
- PySide6 6.5+
- Windows/macOS/Linux

### 安装方式

#### 快速安装
```bash
pip install PySide6
python main.py
```

#### 开发安装
```bash
git clone <repository>
cd ZDEM_Model_Visualization_Editor
pip install -r requirements.txt
python main.py
```

## 🔧 故障排除

### 常见问题

| 问题         | 解决方案                  |
| ------------ | ------------------------- |
| 缺少依赖     | `pip install PySide6`     |
| 图形异常     | 设置 `QT_OPENGL=software` |
| 文件无法打开 | 检查文件格式和权限        |
| 界面卡顿     | 启用异步加载（自动）      |

> 🆘 **详细帮助**: 查看 [用户指南](docs/USER_GUIDE.md#故障排除)

## 📂 项目结构

### 🏗️ 新架构 (推荐)
```
ZDEM_Model_Visualization_Editor/
├── 📦 zdem_editor/          # 主包
│   ├── core/                # 🧠 核心模块
│   │   ├── models.py        # 数据模型
│   │   ├── exceptions.py    # 异常定义
│   │   ├── constants.py     # 常量定义
│   │   └── config.py        # 配置管理
│   ├── parsers/             # 📖 解析器模块
│   │   ├── base.py          # 解析器基类
│   │   └── factory.py       # 解析器工厂
│   ├── ui/                  # 🎨 用户界面
│   │   ├── application.py   # 应用程序类
│   │   └── main_window.py   # 主窗口
│   └── utils/               # 🔧 工具模块
│       ├── logger.py        # 日志系统
│       └── file_utils.py    # 文件工具
├── main_new.py              # 🚀 新程序入口
└── docs/                    # 📚 文档
    └── ARCHITECTURE.md      # 架构文档
```

### 📁 传统结构 (兼容)
```
├── main.py                  # 传统入口
├── models.py                # 数据模型
├── parser.py                # 文件解析
└── ...                      # 其他文件
```

---

## 🎉 开始使用

1. **启动**: `python main.py` 或双击 `start.bat`
2. **加载**: 按 `Ctrl+O` 选择 `sample.zdem`
3. **探索**: 使用鼠标和快捷键操作模型

> 💡 **新手提示**: 建议先阅读 [快速开始指南](docs/QUICK_START.md) 快速上手！
