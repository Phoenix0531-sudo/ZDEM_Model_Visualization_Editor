"""
ZDEM文件解析器
支持动态解析WALL和GLINE对象
"""

import re
from typing import List, Optional, Tuple
from .models import Wall, GLine, PropP4, Point, ZDEMModel
from ..utils.helpers import extract_coordinates, extract_parameters, normalize_color


class ZDEMParser:
    """ZDEM文件解析器"""
    
    def __init__(self):
        self.model = ZDEMModel()
        self.errors = []
    
    def parse_file(self, file_path: str) -> ZDEMModel:
        """解析ZDEM文件"""
        self.model.clear()
        self.errors.clear()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            self._parse_line(line.strip(), line_num)
        
        return self.model
    
    def _parse_line(self, line: str, line_num: int):
        """解析单行内容"""
        if not line or line.startswith('#') or line.startswith('//'):
            return
        
        line_upper = line.upper()
        
        try:
            if line_upper.startswith('WALL'):
                self._parse_wall(line, line_num)
            elif line_upper.startswith('GLINE'):
                self._parse_gline(line, line_num)
            elif line_upper.startswith('PROP') and 'P4' in line_upper:
                self._parse_prop_p4(line, line_num)
        except Exception as e:
            self.errors.append(f"Line {line_num}: {str(e)}")
    
    def _parse_wall(self, line: str, line_num: int):
        """解析WALL对象，支持多种语法格式"""
        # 提取坐标 - 需要在NODES关键字后面查找
        coordinates = self._extract_wall_coordinates(line)
        if len(coordinates) < 2:
            raise ValueError(f"WALL需要至少2个坐标点，找到{len(coordinates)}个")
        
        # 提取参数
        params = extract_parameters(line)
        
        # 创建WALL对象
        wall = Wall(
            id=params.get('id'),
            start_point=Point(coordinates[0][0], coordinates[0][1]),
            end_point=Point(coordinates[1][0], coordinates[1][1]),
            kn=params.get('kn', 0.0),
            ks=params.get('ks', 0.0),
            fric=params.get('fric', 0.0),
            color=normalize_color(params.get('color', 'red')),
            group=params.get('group')
        )
        
        self.model.add_wall(wall)
    
    def _extract_wall_coordinates(self, line: str) -> List[Tuple[float, float]]:
        """专门提取WALL坐标，处理NODES关键字"""
        # 先尝试标准的坐标提取
        coordinates = extract_coordinates(line)
        
        # 如果找到坐标，直接返回
        if coordinates:
            return coordinates
        
        # 如果没找到，可能是因为NODES关键字的存在，尝试更精确的匹配
        # 查找NODES关键字后的坐标
        line_upper = line.upper()
        nodes_match = re.search(r'NODES\s*(.+?)(?:KN|KS|FRIC|COLOR|GROUP|$)', line_upper, re.IGNORECASE)
        if nodes_match:
            nodes_part = nodes_match.group(1)
            coordinates = extract_coordinates(nodes_part)
        
        return coordinates
    
    def _parse_gline(self, line: str, line_num: int):
        """解析GLINE对象"""
        # 提取坐标
        coordinates = extract_coordinates(line)
        if len(coordinates) < 2:
            raise ValueError(f"GLINE需要至少2个坐标点，找到{len(coordinates)}个")
        
        # 提取参数
        params = extract_parameters(line)
        
        # 创建GLINE对象
        gline = GLine(
            start_point=Point(coordinates[0][0], coordinates[0][1]),
            end_point=Point(coordinates[1][0], coordinates[1][1]),
            radius=params.get('radius', 0.0),
            kn=params.get('kn', 0.0),
            ks=params.get('ks', 0.0),
            fric=params.get('fric', 0.0),
            color=normalize_color(params.get('color', 'green')),
            group=params.get('group'),
            cratio=params.get('cratio')
        )
        
        self.model.add_gline(gline)
    
    def _parse_prop_p4(self, line: str, line_num: int):
        """解析PROP P4四边形对象"""
        # 提取坐标 - P4格式需要4个坐标点
        coordinates = extract_coordinates(line)
        if len(coordinates) < 4:
            raise ValueError(f"PROP P4需要至少4个坐标点，找到{len(coordinates)}个")
        
        # 提取参数
        params = extract_parameters(line)
        
        # 解析PROP特有的属性
        prop_info = self._extract_prop_info(line)
        
        # 创建PropP4对象
        points = [Point(coord[0], coord[1]) for coord in coordinates[:4]]  # 只取前4个点
        prop_p4 = PropP4(
            points=points,
            group=params.get('group') or prop_info.get('group'),
            color=normalize_color(params.get('color') or prop_info.get('color', 'orange')),
            property_type=prop_info.get('type', 'group'),
            property_value=prop_info.get('value')
        )
        
        self.model.add_prop_p4(prop_p4)
    
    def _extract_prop_info(self, line: str) -> dict:
        """提取PROP命令的属性信息"""
        info = {}
        line_upper = line.upper()
        
        # 提取属性类型和值
        # 格式：prop group presturct range P4 ...
        # 格式：prop color red range P4 ...
        prop_match = re.search(r'PROP\s+(GROUP|COLOR)\s+(\w+)', line_upper)
        if prop_match:
            info['type'] = prop_match.group(1).lower()
            info['value'] = prop_match.group(2).lower()
            
            if info['type'] == 'group':
                info['group'] = info['value']
            elif info['type'] == 'color':
                info['color'] = info['value']
        
        return info
    
    def get_parse_summary(self) -> str:
        """获取解析摘要"""
        summary = []
        summary.append(f"解析完成:")
        summary.append(f"  - WALL对象: {len(self.model.walls)}个")
        summary.append(f"  - GLINE对象: {len(self.model.glines)}个")
        summary.append(f"  - PROP P4对象: {len(self.model.prop_p4s)}个")
        summary.append(f"  - 总计: {self.model.object_count}个对象")
        
        if self.errors:
            summary.append(f"  - 错误: {len(self.errors)}个")
            for error in self.errors[:5]:  # 只显示前5个错误
                summary.append(f"    {error}")
            if len(self.errors) > 5:
                summary.append(f"    ... 还有{len(self.errors) - 5}个错误")
        
        return '\n'.join(summary)