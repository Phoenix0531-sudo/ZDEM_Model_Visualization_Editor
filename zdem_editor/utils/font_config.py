"""
字体和语言配置
解决中文字体显示问题
"""

import matplotlib
import matplotlib.pyplot as plt
import warnings
import platform
import tkinter as tk
from tkinter import font


def configure_fonts():
    """配置字体设置"""
    # 忽略matplotlib字体警告
    warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
    warnings.filterwarnings('ignore', message='.*Glyph.*missing from font.*')
    
    # 配置matplotlib中文字体
    system = platform.system()
    if system == "Windows":
        # Windows系统字体
        matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    elif system == "Darwin":  # macOS
        # macOS系统字体
        matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'Arial Unicode MS', 'Helvetica', 'DejaVu Sans']
    else:  # Linux
        # Linux系统字体
        matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'DejaVu Sans', 'Liberation Sans']
    
    matplotlib.rcParams['axes.unicode_minus'] = False


def get_system_font():
    """获取系统默认字体"""
    try:
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        default_font = font.nametofont("TkDefaultFont")
        font_family = default_font.actual()['family']
        root.destroy()
        return font_family
    except:
        return "Arial"


# 语言配置
LANGUAGE_CONFIG = {
    'zh': {
        'title': 'ZDEM模型可视化编辑器',
        'file_menu': '文件',
        'open_file': '打开文件...',
        'exit': '退出',
        'view_menu': '视图',
        'refresh': '刷新',
        'fit_window': '适应窗口',
        'clear_selection': '清除选择',
        'help_menu': '帮助',
        'about': '关于',
        'open_file_btn': '打开文件',
        'model_info': '模型信息',
        'object_list': '对象列表',
        'object_col': '对象',
        'type_col': '类型',
        'details_col': '详情',
        'ready': '就绪',
        'loading': '正在解析文件...',
        'loaded': '已加载',
        'objects': '个对象',
        'load_failed': '加载失败',
        'error': '错误',
        'load_error': '加载文件失败',
        'select_file': '选择ZDEM文件',
        'empty_canvas': '请打开ZDEM文件',
        'x_coord': 'X坐标',
        'y_coord': 'Y坐标',
        'selected': '已选择',
        'container': '容器',
        'wall_objects': '墙体对象',
        'gline_objects': '几何线段',
    },
    'en': {
        'title': 'ZDEM Model Visualization Editor',
        'file_menu': 'File',
        'open_file': 'Open File...',
        'exit': 'Exit',
        'view_menu': 'View',
        'refresh': 'Refresh',
        'fit_window': 'Fit Window',
        'clear_selection': 'Clear Selection',
        'help_menu': 'Help',
        'about': 'About',
        'open_file_btn': 'Open File',
        'model_info': 'Model Info',
        'object_list': 'Object List',
        'object_col': 'Object',
        'type_col': 'Type',
        'details_col': 'Details',
        'ready': 'Ready',
        'loading': 'Parsing file...',
        'loaded': 'Loaded',
        'objects': ' objects',
        'load_failed': 'Load failed',
        'error': 'Error',
        'load_error': 'Failed to load file',
        'select_file': 'Select ZDEM File',
        'empty_canvas': 'Please open a ZDEM file',
        'x_coord': 'X Coordinate',
        'y_coord': 'Y Coordinate',
        'selected': 'Selected',
        'container': 'Container',
        'wall_objects': 'Wall Objects',
        'gline_objects': 'Geometry Lines',
    }
}

# 默认使用英文以避免字体问题
CURRENT_LANGUAGE = 'en'


def get_text(key: str) -> str:
    """获取当前语言的文本"""
    return LANGUAGE_CONFIG[CURRENT_LANGUAGE].get(key, key)


def set_language(lang: str):
    """设置语言"""
    global CURRENT_LANGUAGE
    if lang in LANGUAGE_CONFIG:
        CURRENT_LANGUAGE = lang