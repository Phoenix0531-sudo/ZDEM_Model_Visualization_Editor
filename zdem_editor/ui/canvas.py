"""
ZDEM模型可视化画布
使用matplotlib实现第一象限坐标系显示
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from typing import Optional, Tuple

from ..core.models import ZDEMModel, Wall, GLine, PropP4
from ..utils.helpers import calculate_view_bounds
from ..utils.font_config import configure_fonts, get_text

# 配置字体
configure_fonts()


class ZDEMCanvas:
    """ZDEM模型可视化画布"""
    
    def __init__(self, parent):
        self.parent = parent
        self.model: Optional[ZDEMModel] = None
        self.selected_object_ids = set()  # 存储选中对象的ID
        self.object_lines = {}  # 存储对象到matplotlib线条的映射
        
        # 创建matplotlib图形
        self.figure = Figure(figsize=(10, 8), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # 创建tkinter画布
        self.canvas = FigureCanvasTkAgg(self.figure, parent)
        self.canvas_widget = self.canvas.get_tk_widget()
        
        # 设置样式
        self.figure.patch.set_facecolor('white')
        self.ax.set_facecolor('#f8f8f8')
        
        # 初始化显示
        self._setup_coordinate_system()
        self._draw_empty_canvas()
    
    def _setup_coordinate_system(self):
        """设置第一象限坐标系"""
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('X Coordinate', fontsize=10)
        self.ax.set_ylabel('Y Coordinate', fontsize=10)
        
        # 确保Y轴向上
        self.ax.invert_yaxis()
        self.ax.invert_yaxis()  # 双重反转确保正确
    
    def _draw_empty_canvas(self):
        """绘制空画布"""
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.text(50, 50, 'Please open a ZDEM file', 
                    ha='center', va='center', fontsize=14, alpha=0.5)
        self.canvas.draw()
    
    def set_model(self, model: ZDEMModel):
        """设置要显示的模型"""
        self.model = model
        self.refresh()
    
    def refresh(self):
        """刷新显示"""
        if not self.model or self.model.object_count == 0:
            self._draw_empty_canvas()
            return
        
        self._setup_coordinate_system()
        self.object_lines.clear()  # 清空对象线条映射
        self._draw_model()
        self._setup_view_bounds()
        self.canvas.draw()
    
    def _draw_model(self):
        """绘制模型对象"""
        # 绘制WALL对象
        for wall in self.model.walls:
            self._draw_wall(wall)
        
        # 绘制GLINE对象
        for gline in self.model.glines:
            self._draw_gline(gline)
        
        # 绘制PROP P4对象
        for prop_p4 in self.model.prop_p4s:
            self._draw_prop_p4(prop_p4)
    
    def _get_object_id(self, obj):
        """获取对象的唯一标识符"""
        if isinstance(obj, Wall):
            return f"wall_{id(obj)}"
        elif isinstance(obj, GLine):
            return f"gline_{id(obj)}"
        elif isinstance(obj, PropP4):
            return f"prop_p4_{id(obj)}"
        else:
            return f"unknown_{id(obj)}"
    
    def _draw_wall(self, wall: Wall):
        """绘制WALL对象"""
        x_coords = [wall.start_point.x, wall.end_point.x]
        y_coords = [wall.start_point.y, wall.end_point.y]
        
        # 检查是否被选中
        obj_id = self._get_object_id(wall)
        is_selected = obj_id in self.selected_object_ids
        linewidth = 5 if is_selected else 3
        alpha = 1.0 if is_selected else 0.8
        
        # 绘制主线条
        line, = self.ax.plot(x_coords, y_coords, 
                            color=wall.color, 
                            linewidth=linewidth,
                            alpha=alpha,
                            solid_capstyle='round',
                            label=f'WALL {wall.id or ""}' if wall.id else None)
        
        # 添加端点标记
        points, = self.ax.plot(x_coords, y_coords, 'o', 
                              color=wall.color, 
                              markersize=6 if is_selected else 4,
                              alpha=alpha)
        
        # 如果被选中，添加高亮边框
        if is_selected:
            highlight_line, = self.ax.plot(x_coords, y_coords, 
                                          color='yellow', 
                                          linewidth=7,
                                          alpha=0.6,
                                          solid_capstyle='round',
                                          zorder=line.get_zorder() - 1)
            self.object_lines[obj_id] = [highlight_line, line, points]
        else:
            self.object_lines[obj_id] = [line, points]
    
    def _draw_gline(self, gline: GLine):
        """绘制GLINE对象"""
        x_coords = [gline.start_point.x, gline.end_point.x]
        y_coords = [gline.start_point.y, gline.end_point.y]
        
        # 检查是否被选中
        obj_id = self._get_object_id(gline)
        is_selected = obj_id in self.selected_object_ids
        
        # 根据半径调整线宽
        base_linewidth = max(1, min(gline.radius / 20, 5)) if gline.radius > 0 else 2
        linewidth = base_linewidth + 1 if is_selected else base_linewidth
        alpha = 1.0 if is_selected else 0.8
        
        # 绘制主线条
        line, = self.ax.plot(x_coords, y_coords, 
                            color=gline.color, 
                            linewidth=linewidth,
                            linestyle='-',
                            alpha=alpha)
        
        # 添加端点标记
        points, = self.ax.plot(x_coords, y_coords, 's', 
                              color=gline.color, 
                              markersize=5 if is_selected else 3,
                              alpha=alpha)
        
        # 如果被选中，添加高亮边框
        if is_selected:
            highlight_line, = self.ax.plot(x_coords, y_coords, 
                                          color='yellow', 
                                          linewidth=linewidth + 2,
                                          alpha=0.6,
                                          linestyle='-',
                                          zorder=line.get_zorder() - 1)
            self.object_lines[obj_id] = [highlight_line, line, points]
        else:
            self.object_lines[obj_id] = [line, points]
    
    def _draw_prop_p4(self, prop_p4: PropP4):
        """绘制PROP P4四边形对象"""
        # 提取四个顶点的坐标
        x_coords = [p.x for p in prop_p4.points] + [prop_p4.points[0].x]  # 闭合多边形
        y_coords = [p.y for p in prop_p4.points] + [prop_p4.points[0].y]  # 闭合多边形
        
        # 检查是否被选中
        obj_id = self._get_object_id(prop_p4)
        is_selected = obj_id in self.selected_object_ids
        
        # 设置样式
        linewidth = 3 if is_selected else 2
        alpha = 0.7 if is_selected else 0.5
        edge_alpha = 1.0 if is_selected else 0.8
        
        # 绘制填充的四边形
        polygon = self.ax.fill(x_coords, y_coords, 
                              color=prop_p4.color, 
                              alpha=alpha,
                              edgecolor=prop_p4.color,
                              linewidth=linewidth,
                              linestyle='-')
        
        # 绘制边框
        edge_line, = self.ax.plot(x_coords, y_coords, 
                                 color=prop_p4.color, 
                                 linewidth=linewidth,
                                 alpha=edge_alpha,
                                 linestyle='-')
        
        # 添加顶点标记
        points, = self.ax.plot([p.x for p in prop_p4.points], 
                              [p.y for p in prop_p4.points], 
                              'D',  # 菱形标记
                              color=prop_p4.color, 
                              markersize=6 if is_selected else 4,
                              alpha=edge_alpha)
        
        # 如果被选中，添加高亮边框
        if is_selected:
            highlight_line, = self.ax.plot(x_coords, y_coords, 
                                          color='yellow', 
                                          linewidth=linewidth + 2,
                                          alpha=0.8,
                                          linestyle='-',
                                          zorder=edge_line.get_zorder() + 1)
            self.object_lines[obj_id] = [polygon[0], highlight_line, edge_line, points]
        else:
            self.object_lines[obj_id] = [polygon[0], edge_line, points]
    
    def _setup_view_bounds(self):
        """设置视图边界"""
        if not self.model:
            return
        
        model_bounds = self.model.bounds
        view_bounds = calculate_view_bounds(model_bounds, padding_ratio=0.15)
        
        self.ax.set_xlim(view_bounds[0], view_bounds[2])
        self.ax.set_ylim(view_bounds[1], view_bounds[3])
        
        # 添加坐标标注
        self._add_coordinate_labels(view_bounds)
    
    def _add_coordinate_labels(self, bounds: Tuple[float, float, float, float]):
        """添加坐标标注"""
        min_x, min_y, max_x, max_y = bounds
        
        # 计算合适的刻度间隔
        x_range = max_x - min_x
        y_range = max_y - min_y
        
        # 动态计算刻度间隔
        x_step = self._calculate_tick_step(x_range)
        y_step = self._calculate_tick_step(y_range)
        
        # 设置刻度
        x_ticks = np.arange(
            int(min_x / x_step) * x_step,
            int(max_x / x_step + 1) * x_step,
            x_step
        )
        y_ticks = np.arange(
            int(min_y / y_step) * y_step,
            int(max_y / y_step + 1) * y_step,
            y_step
        )
        
        self.ax.set_xticks(x_ticks)
        self.ax.set_yticks(y_ticks)
        
        # 格式化刻度标签
        self.ax.tick_params(axis='both', which='major', labelsize=8)
    
    def _calculate_tick_step(self, range_val: float) -> float:
        """计算合适的刻度间隔"""
        if range_val <= 0:
            return 1
        
        # 基于范围大小选择合适的步长
        magnitude = 10 ** int(np.log10(range_val))
        normalized = range_val / magnitude
        
        if normalized <= 1:
            step = 0.2 * magnitude
        elif normalized <= 2:
            step = 0.5 * magnitude
        elif normalized <= 5:
            step = 1 * magnitude
        else:
            step = 2 * magnitude
        
        return max(step, 1)
    
    def select_object(self, obj):
        """选中单个对象"""
        self.selected_object_ids.clear()
        obj_id = self._get_object_id(obj)
        self.selected_object_ids.add(obj_id)
        self.refresh()
    
    def select_objects(self, objects):
        """选中多个对象"""
        self.selected_object_ids.clear()
        for obj in objects:
            obj_id = self._get_object_id(obj)
            self.selected_object_ids.add(obj_id)
        self.refresh()
    
    def clear_selection(self):
        """清除所有选择"""
        self.selected_object_ids.clear()
        self.refresh()
    
    def get_widget(self):
        """获取tkinter组件"""
        return self.canvas_widget