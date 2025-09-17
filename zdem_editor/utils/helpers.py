"""
辅助工具函数
提供解析和处理相关的工具函数
"""

import re
from typing import List, Tuple, Dict, Any


def extract_coordinates(text: str) -> List[Tuple[float, float]]:
    """
    从文本中提取坐标点，支持中英文括号和P1/P2格式
    支持格式：
    - (x, y) （x, y） [x, y] 【x, y】
    - P1 (x, y) P2 (x, y)
    - nodes (x, y) (x, y)
    """
    coordinates = []
    
    # 首先尝试P1/P2格式
    p1_p2_coords = extract_p1_p2_coordinates(text)
    if p1_p2_coords:
        coordinates.extend(p1_p2_coords)
        return coordinates
    
    # 支持多种括号格式
    bracket_patterns = [
        r'\(\s*([-+]?\d*\.?\d+)\s*[,\s]\s*([-+]?\d*\.?\d+)\s*\)',  # (x, y)
        r'（\s*([-+]?\d*\.?\d+)\s*[,\s]\s*([-+]?\d*\.?\d+)\s*）',  # （x, y）
        r'\[\s*([-+]?\d*\.?\d+)\s*[,\s]\s*([-+]?\d*\.?\d+)\s*\]',  # [x, y]
        r'【\s*([-+]?\d*\.?\d+)\s*[,\s]\s*([-+]?\d*\.?\d+)\s*】',  # 【x, y】
    ]
    
    for pattern in bracket_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                x, y = float(match[0]), float(match[1])
                coordinates.append((x, y))
            except (ValueError, IndexError):
                continue
    
    return coordinates


def extract_p1_p2_coordinates(text: str) -> List[Tuple[float, float]]:
    """
    专门提取P1/P2格式的坐标
    格式：P1 (x, y) P2 (x, y)
    """
    coordinates = []
    
    # P1坐标模式
    p1_pattern = r'P1\s*\(\s*([-+]?\d*\.?\d+)\s*[,\s]\s*([-+]?\d*\.?\d+)\s*\)'
    p1_match = re.search(p1_pattern, text, re.IGNORECASE)
    
    # P2坐标模式
    p2_pattern = r'P2\s*\(\s*([-+]?\d*\.?\d+)\s*[,\s]\s*([-+]?\d*\.?\d+)\s*\)'
    p2_match = re.search(p2_pattern, text, re.IGNORECASE)
    
    if p1_match and p2_match:
        try:
            p1_x, p1_y = float(p1_match.group(1)), float(p1_match.group(2))
            p2_x, p2_y = float(p2_match.group(1)), float(p2_match.group(2))
            coordinates.append((p1_x, p1_y))
            coordinates.append((p2_x, p2_y))
        except (ValueError, IndexError):
            pass
    
    return coordinates


def extract_parameters(text: str) -> Dict[str, Any]:
    """
    从文本中提取参数
    支持多种WALL和GLINE语法格式，增强鲁棒性
    """
    params = {}
    
    # 参数模式：支持多种格式
    param_patterns = [
        # WALL ID格式：ID 1, id 1, ID=1, id=1, ID 0
        (r'ID\s*=?\s*(\d+)', 'id'),
        
        # 半径格式：RAD=0.5, R=0.5, r 80.0, r=80.0
        (r'(?:RAD|R)\s*=?\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', 'radius'),
        
        # 刚度系数格式：KN=1.0, kn= 11.2e9, KN 1.0
        (r'KN\s*=?\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', 'kn'),
        (r'KS\s*=?\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', 'ks'),
        
        # 摩擦系数格式：FRIC=0.5, fric 0.00, FRIC 0.5, fric=0.00
        (r'FRIC\s*=?\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', 'fric'),
        
        # 其他参数
        (r'CRATIO\s*=?\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', 'cratio'),
        
        # 颜色格式：COLOR=red, color red, color=blue, color=1 (支持数字颜色)
        (r'COLOR\s*=?\s*(\w+)', 'color'),
        
        # 组格式：GROUP=wall1, group fault, GROUP fault1
        (r'GROUP\s*=?\s*(\w+)', 'group'),
    ]
    
    text_upper = text.upper()
    
    for pattern, param_name in param_patterns:
        match = re.search(pattern, text_upper)
        if match:
            value = match.group(1)
            if param_name in ['radius', 'kn', 'ks', 'fric', 'cratio']:
                try:
                    params[param_name] = float(value)
                except ValueError:
                    continue
            elif param_name == 'id':
                try:
                    params[param_name] = int(value)
                except ValueError:
                    continue
            else:
                params[param_name] = value.lower()
    
    return params


def normalize_color(color_str: str) -> str:
    """
    标准化颜色名称，支持数字颜色
    """
    if not color_str:
        return "black"
    
    # 处理数字颜色
    if color_str.isdigit():
        color_num = int(color_str)
        # 数字颜色映射
        number_color_map = {
            0: 'black',
            1: 'red', 
            2: 'green',
            3: 'blue',
            4: 'yellow',
            5: 'magenta',
            6: 'cyan',
            7: 'white',
            8: 'orange',
            9: 'purple'
        }
        return number_color_map.get(color_num, 'black')
    
    # 处理文字颜色
    color_map = {
        'red': 'red',
        'green': 'green',
        'blue': 'blue',
        'yellow': 'yellow',
        'black': 'black',
        'white': 'white',
        'gray': 'gray',
        'grey': 'gray',
        'orange': 'orange',
        'purple': 'purple',
        'pink': 'pink',
        'brown': 'brown',
        'magenta': 'magenta',
        'mg': 'magenta',
        'cyan': 'cyan',
        'lg': 'lightgreen',
        'gb': 'lightblue'
    }
    
    return color_map.get(color_str.lower(), color_str.lower())


def calculate_view_bounds(model_bounds: Tuple[float, float, float, float], 
                         padding_ratio: float = 0.1) -> Tuple[float, float, float, float]:
    """
    计算视图边界，添加适当的留白
    """
    min_x, min_y, max_x, max_y = model_bounds
    
    width = max_x - min_x
    height = max_y - min_y
    
    # 确保最小尺寸
    if width < 1:
        width = 100
    if height < 1:
        height = 100
    
    padding_x = width * padding_ratio
    padding_y = height * padding_ratio
    
    return (
        min_x - padding_x,
        min_y - padding_y,
        max_x + padding_x,
        max_y + padding_y
    )