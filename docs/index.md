# ZDEM Model Visualization Editor

<div align="center">

A PySide6-based tool for visualizing and editing ZDEM model files.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySide6](https://img.shields.io/badge/PySide-6.5%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

## Overview

Interactive graphical editor for ZDEM model files. Supports WALL, GLINE, BOX, and PROP P4 object types with real-time rendering, selection highlighting, and asynchronous file loading.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Docker

```bash
docker build -t zdem-editor .
docker run --rm zdem-editor python -c "from zdem_editor.core.models import ZDEMModel; print('OK')"
```

*Docker is for build verification only; GUI requires a native display environment.*

## Repository

<https://github.com/Phoenix0531-sudo/ZDEM_Model_Visualization_Editor>

## License

MIT License
