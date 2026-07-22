# ZDEM Model Editor

**Visual editor for ZDEM model structure files — tkinter + matplotlib canvas.**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Edit model geometry/structure with visual feedback instead of pure text. Application code under `zdem_editor/` (core parsers + canvas).  

**Important path split:**

| Path | Meaning |
|------|---------|
| `Test/` | ZDEM **DSL sample scripts** (not pytest) — excluded from ruff |
| `tests/` | Real pytest (e.g. parser smoke) |

## Preview

![ZDEM Model Editor](docs/screenshots/preview.png)

## Install / run

```bash
git clone https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor.git
cd ZDEM_Model_Editor
pip install -r requirements.txt
python main.py
pytest tests/
```

## License

MIT. See [LICENSE](LICENSE).
