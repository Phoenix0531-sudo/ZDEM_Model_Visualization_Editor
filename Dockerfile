# Build/test environment only — GUI requires display server (X11/Wayland)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for tkinter and matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    tk-dev \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Smoke test: verify imports (GUI will not render in Docker)
CMD python -c "
import sys
import tkinter
print('tkinter:', tkinter.TkVersion)
import matplotlib
print('matplotlib:', matplotlib.__version__)
import numpy
print('numpy:', numpy.__version__)
from zdem_editor.ui.canvas import ZDEMCanvas
print('ZDEMCanvas import OK')
from zdem_editor.core.models import ZDEMModel
from zdem_editor.core.parser import ZDEMParser
print('All imports OK')
"
