"""Docker build-time smoke test: verify all imports succeed."""
import sys
import tkinter
print(f"tkinter: {tkinter.TkVersion}")

import matplotlib
print(f"matplotlib: {matplotlib.__version__}")

import numpy
print(f"numpy: {numpy.__version__}")

from zdem_editor.ui.canvas import ZDEMCanvas
print("ZDEMCanvas import OK")

from zdem_editor.core.models import ZDEMModel, Wall, GLine, PropP4
from zdem_editor.core.parser import ZDEMParser
print("All imports OK")
