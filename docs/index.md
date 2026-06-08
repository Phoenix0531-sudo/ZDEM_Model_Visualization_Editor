# ZDEM Model Visualization Editor

<div align="center">

A tkinter + matplotlib tool for visualizing and editing ZDEM model files.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-8.5%2B-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

## Overview

Interactive graphical editor for ZDEM model files. Supports WALL, GLINE, BOX, and PROP P4 object types with real-time rendering via matplotlib, selection highlighting, and asynchronous file loading.

## Quick Start

```bash
pip install matplotlib numpy
python main.py
```

## Docker

```bash
docker build -t zdem-editor .
docker run --rm zdem-editor
```

*Docker is for build verification only; GUI requires a native display environment.*

## Repository

<https://github.com/Phoenix0531-sudo/ZDEM_Model_Visualization_Editor>

## License

MIT License
