# ZDEM Model Editor

**ZDEM 模型文件可视化编辑器 — tkinter + matplotlib。**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

代码在 `zdem_editor/`。**`Test/` = ZDEM DSL 样例（非 pytest）**；**`tests/` = 真测试**。ruff 排除 DSL 树。

## 安装 / 运行

```bash
pip install -r requirements.txt
python main.py
```

启动后：**File → Open File...（Ctrl+O）** 加载一个 ZDEM DSL 脚本——`Test/` 里的样例（如 `Test/gen0.py`、`Test/shear0.py`）开箱即用。画布渲染墙体、几何线与 P4 多边形；Object List 页按类型分组所有实体，选中即在画布高亮。`View → Refresh（F5）` 从磁盘重新加载当前文件。

解析器测试套件在 `tests/`：

```bash
pytest -q tests
```

## 许可证

MIT。详见 [LICENSE](LICENSE)。
