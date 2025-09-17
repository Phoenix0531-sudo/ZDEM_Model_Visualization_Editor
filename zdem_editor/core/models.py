"""
数据模型定义
定义WALL、GLINE等对象的数据结构
"""

from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass
class Point:
    """二维坐标点"""
    x: float
    y: float
    
    def __iter__(self):
        return iter((self.x, self.y))


@dataclass
class Wall:
    """墙体对象"""
    id: Optional[int]
    start_point: Point
    end_point: Point
    kn: float = 0.0
    ks: float = 0.0
    fric: float = 0.0
    color: str = "red"
    group: Optional[str] = None
    
    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """返回边界框 (min_x, min_y, max_x, max_y)"""
        return (
            min(self.start_point.x, self.end_point.x),
            min(self.start_point.y, self.end_point.y),
            max(self.start_point.x, self.end_point.x),
            max(self.start_point.y, self.end_point.y)
        )


@dataclass
class GLine:
    """几何线段对象"""
    start_point: Point
    end_point: Point
    radius: float = 0.0
    kn: float = 0.0
    ks: float = 0.0
    fric: float = 0.0
    color: str = "green"
    group: Optional[str] = None
    cratio: Optional[float] = None
    
    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """返回边界框 (min_x, min_y, max_x, max_y)"""
        return (
            min(self.start_point.x, self.end_point.x),
            min(self.start_point.y, self.end_point.y),
            max(self.start_point.x, self.end_point.x),
            max(self.start_point.y, self.end_point.y)
        )


@dataclass
class PropP4:
    """PROP P4四边形对象"""
    points: List[Point]  # 四个顶点
    group: Optional[str] = None
    color: str = "orange"
    property_type: str = "group"  # group, color等
    property_value: Optional[str] = None
    
    def __post_init__(self):
        """确保有4个点"""
        if len(self.points) != 4:
            raise ValueError(f"P4四边形需要4个点，提供了{len(self.points)}个")
    
    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """返回边界框 (min_x, min_y, max_x, max_y)"""
        x_coords = [p.x for p in self.points]
        y_coords = [p.y for p in self.points]
        return (
            min(x_coords),
            min(y_coords),
            max(x_coords),
            max(y_coords)
        )


class ZDEMModel:
    """ZDEM模型数据容器"""
    
    def __init__(self):
        self.walls: List[Wall] = []
        self.glines: List[GLine] = []
        self.prop_p4s: List[PropP4] = []
        self._bounds_cache = None
    
    def add_wall(self, wall: Wall):
        """添加墙体对象"""
        self.walls.append(wall)
        self._bounds_cache = None
    
    def add_gline(self, gline: GLine):
        """添加几何线段对象"""
        self.glines.append(gline)
        self._bounds_cache = None
    
    def add_prop_p4(self, prop_p4: PropP4):
        """添加P4四边形对象"""
        self.prop_p4s.append(prop_p4)
        self._bounds_cache = None
    
    def clear(self):
        """清空所有对象"""
        self.walls.clear()
        self.glines.clear()
        self.prop_p4s.clear()
        self._bounds_cache = None
    
    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """获取所有对象的边界框"""
        if self._bounds_cache is not None:
            return self._bounds_cache
        
        if not self.walls and not self.glines and not self.prop_p4s:
            return (0, 0, 100, 100)  # 默认边界
        
        all_bounds = []
        for wall in self.walls:
            all_bounds.append(wall.bounds)
        for gline in self.glines:
            all_bounds.append(gline.bounds)
        for prop_p4 in self.prop_p4s:
            all_bounds.append(prop_p4.bounds)
        
        min_x = min(bounds[0] for bounds in all_bounds)
        min_y = min(bounds[1] for bounds in all_bounds)
        max_x = max(bounds[2] for bounds in all_bounds)
        max_y = max(bounds[3] for bounds in all_bounds)
        
        self._bounds_cache = (min_x, min_y, max_x, max_y)
        return self._bounds_cache
    
    @property
    def object_count(self) -> int:
        """获取对象总数"""
        return len(self.walls) + len(self.glines) + len(self.prop_p4s)
    
    def get_all_objects(self) -> List:
        """获取所有对象的列表"""
        return self.walls + self.glines + self.prop_p4s