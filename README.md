# ZDEM Model Editor

**Visual editor for ZDEM model files (tkinter + matplotlib).**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Edit structure files visually. Test/ holds DSL samples, not pytest.

## Preview

![ZDEM Model Editor](docs/screenshots/preview.png)

## Features

- Visual editing under zdem_editor/
- matplotlib canvases for geometry feedback
- Real pytest under tests/ (parser smoke)
- Ruff excludes ZDEM DSL sample trees

## Get started

### Install

```bash
git clone https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor.git
cd ZDEM_Model_Editor
pip install -r requirements.txt
```

### Usage

```bash
python main.py
pytest tests/
```

## Project layout

```
main.py  zdem_editor/
Test/    # DSL samples
tests/   # real pytest
```

## Related ZDEM tools

| Repo | Role |
|------|------|
| [ZDEM_ParticleTracker](https://github.com/Phoenix0531-sudo/ZDEM_ParticleTracker) | Interactive particle tracking + true-radius render |
| [ZDEM_Salt_Kinematics](https://github.com/Phoenix0531-sudo/ZDEM_Salt_Kinematics) | Salt geometry / kinematics extraction and plots |
| [ZDEM_Area_Conservation](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation) | Area-conservation / triangulation analysis |
| [ZDEM_Bond_Fracture](https://github.com/Phoenix0531-sudo/ZDEM_Bond_Fracture) | Bond damage series + visualizer |
| [ZDEM_Damage_Thresholds](https://github.com/Phoenix0531-sudo/ZDEM_Damage_Thresholds) | Damage thresholds and energy plots |
| [ZDEM_DFN](https://github.com/Phoenix0531-sudo/ZDEM_DFN) | Discrete fracture network generator |
| [ZDEM_Model_Editor](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor) | Model file visual editor |
| [ZDEM_Archiver](https://github.com/Phoenix0531-sudo/ZDEM_Archiver) | Archive / purge bulky dumps |
| [ZDEM3D_WEB](https://github.com/Phoenix0531-sudo/ZDEM3D_WEB) | CAE cloud UI (Django + React + VTK.js) |


## Notes

Desktop editor for model authors.

## License

MIT. Free for commercial use with attribution where applicable. See [LICENSE](LICENSE).
