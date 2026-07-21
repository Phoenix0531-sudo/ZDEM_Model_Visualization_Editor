# ZDEM Model Editor

**tkinter + matplotlib 的 ZDEM 模型文件编辑器**

[English](README.md) | [中文](README.zh-CN.md)

![CI](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

tkinter + matplotlib 的 ZDEM 模型文件编辑器。

> 作者：[Phoenix0531-sudo](https://github.com/Phoenix0531-sudo) · 欢迎学习、二次开发与**商业使用**，请保留本仓库署名与许可证声明。

## 技术栈

Python · tkinter · matplotlib

## 功能特性

- 模型文件编辑
- 交互绘图
- Test/ 样例

## 快速开始

```bash
git clone https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor.git
cd ZDEM_Model_Editor
```

```bash
pip install -r requirements.txt
python main.py
```

更完整的英文说明见 [README.md](README.md)。

## 仓库结构（摘要）

```
ZDEM_Model_Editor/
├─ .github/
├─ docs/
├─ scripts/
├─ Test/
├─ zdem_editor/
├─ CHANGELOG.md
├─ Dockerfile
├─ LICENSE
├─ main.py
├─ README.md
├─ README.zh-CN.md
├─ requirements.txt
```

## 测试

```bash
pip install pytest
pytest -q
```

仓库内 `tests/` 至少包含 smoke 测试；有完整测试套件时以 CI 为准。

## CI

GitHub Actions（`push` / `pull_request`）会：

- 安装依赖（requirements / pyproject）
- 运行 `pytest`（**硬失败**）
- 尽力做语法/结构检查

## 许可证

[MIT](LICENSE) — 可自由使用、修改、分发与**商用**，需保留版权与许可声明（提及本仓库 / 作者即可）。

## 关于

维护者：[Phoenix0531-sudo](https://github.com/Phoenix0531-sudo)
