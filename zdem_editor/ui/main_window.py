"""
主窗口界面
提供文件操作和模型显示功能
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from typing import Optional

from ..core.parser import ZDEMParser
from ..core.models import ZDEMModel
from .canvas import ZDEMCanvas


class MainWindow:
    """主窗口类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.parser = ZDEMParser()
        self.current_model: Optional[ZDEMModel] = None
        self.current_file: Optional[str] = None
        self.tree_item_to_object = {}  # 树形控件项目到对象的映射
        
        self._setup_window()
        self._create_menu()
        self._create_widgets()
        self._setup_layout()
        
    def _setup_window(self):
        """设置窗口属性"""
        self.root.title("ZDEM模型可视化编辑器")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # 设置图标（如果有的话）
        try:
            # self.root.iconbitmap("icon.ico")
            pass
        except:
            pass
    
    def _create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="打开文件...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit, accelerator="Ctrl+Q")
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="刷新", command=self.refresh_view, accelerator="F5")
        view_menu.add_command(label="适应窗口", command=self.fit_view, accelerator="Ctrl+F")
        view_menu.add_separator()
        view_menu.add_command(label="清除选择", command=self.clear_selection, accelerator="Esc")
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
        
        # 绑定快捷键
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F5>', lambda e: self.refresh_view())
        self.root.bind('<Control-f>', lambda e: self.fit_view())
        self.root.bind('<Escape>', lambda e: self.clear_selection())
    
    def _create_widgets(self):
        """创建界面组件"""
        # 主框架
        self.main_frame = ttk.Frame(self.root)
        
        # 工具栏
        self.toolbar = ttk.Frame(self.main_frame)
        self.open_btn = ttk.Button(self.toolbar, text="打开文件", command=self.open_file)
        self.refresh_btn = ttk.Button(self.toolbar, text="刷新", command=self.refresh_view)
        
        # 内容区域 - 使用PanedWindow分割
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        
        # 左侧面板 - 信息显示
        self.left_panel = ttk.Frame(self.paned_window, width=300)
        self.info_notebook = ttk.Notebook(self.left_panel)
        
        # 模型信息标签页
        self.info_frame = ttk.Frame(self.info_notebook)
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=15, width=35)
        self.info_notebook.add(self.info_frame, text="模型信息")
        
        # 对象列表标签页
        self.objects_frame = ttk.Frame(self.info_notebook)
        self.objects_tree = ttk.Treeview(self.objects_frame, columns=('type', 'details'), show='tree headings')
        self.objects_tree.heading('#0', text='对象')
        self.objects_tree.heading('type', text='类型')
        self.objects_tree.heading('details', text='详情')
        self.objects_scrollbar = ttk.Scrollbar(self.objects_frame, orient=tk.VERTICAL, command=self.objects_tree.yview)
        self.objects_tree.configure(yscrollcommand=self.objects_scrollbar.set)
        
        # 绑定对象列表选择事件
        self.objects_tree.bind('<<TreeviewSelect>>', self._on_object_select)
        
        self.info_notebook.add(self.objects_frame, text="对象列表")
        
        # 右侧面板 - 画布
        self.right_panel = ttk.Frame(self.paned_window)
        self.canvas = ZDEMCanvas(self.right_panel)
        
        # 状态栏
        self.status_bar = ttk.Frame(self.main_frame)
        self.status_label = ttk.Label(self.status_bar, text="就绪")
        
        # 添加面板到PanedWindow
        self.paned_window.add(self.left_panel, weight=1)
        self.paned_window.add(self.right_panel, weight=3)
    
    def _setup_layout(self):
        """设置布局"""
        # 主框架
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 工具栏
        self.toolbar.pack(fill=tk.X, pady=(0, 5))
        self.open_btn.pack(side=tk.LEFT, padx=(0, 5))
        self.refresh_btn.pack(side=tk.LEFT)
        
        # 内容区域
        self.paned_window.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # 左侧面板布局
        self.info_notebook.pack(fill=tk.BOTH, expand=True, padx=(0, 5))
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 对象列表布局
        self.objects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        self.objects_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
        
        # 右侧面板布局
        self.canvas.get_widget().pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_bar.pack(fill=tk.X)
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # 初始化信息显示
        self._update_info_display()
    
    def open_file(self):
        """打开文件对话框"""
        file_path = filedialog.askopenfilename(
            title="选择ZDEM文件",
            filetypes=[
                ("Python文件", "*.py"),
                ("ZDEM文件", "*.zdem"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path: str):
        """加载文件"""
        try:
            self.status_label.config(text="正在解析文件...")
            self.root.update()
            
            # 解析文件
            self.current_model = self.parser.parse_file(file_path)
            self.current_file = file_path
            
            # 更新显示
            self.canvas.set_model(self.current_model)
            self._update_info_display()
            self._update_objects_tree()
            
            # 更新状态
            filename = os.path.basename(file_path)
            self.status_label.config(text=f"已加载: {filename} - {self.current_model.object_count}个对象")
            self.root.title(f"ZDEM模型可视化编辑器 - {filename}")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载文件失败:\n{str(e)}")
            self.status_label.config(text="加载失败")
    
    def refresh_view(self):
        """刷新视图"""
        if self.current_file:
            self.load_file(self.current_file)
        else:
            self.canvas.refresh()
    
    def fit_view(self):
        """适应视图"""
        self.canvas.refresh()
    
    def _update_info_display(self):
        """更新信息显示"""
        self.info_text.delete(1.0, tk.END)
        
        if self.current_model:
            info = self.parser.get_parse_summary()
            if self.current_file:
                info = f"文件: {os.path.basename(self.current_file)}\n\n" + info
            
            # 添加边界信息
            bounds = self.current_model.bounds
            info += f"\n\n边界信息:"
            info += f"\n  X范围: {bounds[0]:.2f} ~ {bounds[2]:.2f}"
            info += f"\n  Y范围: {bounds[1]:.2f} ~ {bounds[3]:.2f}"
            info += f"\n  宽度: {bounds[2] - bounds[0]:.2f}"
            info += f"\n  高度: {bounds[3] - bounds[1]:.2f}"
            
        else:
            info = "未加载模型文件\n\n请使用 文件 -> 打开文件 来加载ZDEM模型"
        
        self.info_text.insert(1.0, info)
    
    def _update_objects_tree(self):
        """更新对象列表"""
        # 清空现有项目和映射
        for item in self.objects_tree.get_children():
            self.objects_tree.delete(item)
        self.tree_item_to_object.clear()
        
        if not self.current_model:
            return
        
        # 添加WALL对象
        if self.current_model.walls:
            wall_root = self.objects_tree.insert('', 'end', text=f'WALL ({len(self.current_model.walls)})', 
                                               values=('容器', '墙体对象'))
            for i, wall in enumerate(self.current_model.walls):
                details = f"({wall.start_point.x:.1f},{wall.start_point.y:.1f}) -> ({wall.end_point.x:.1f},{wall.end_point.y:.1f})"
                item_id = self.objects_tree.insert(wall_root, 'end', text=f'Wall {wall.id or i+1}', 
                                                 values=('WALL', details))
                # 建立树形控件项目到对象的映射
                self.tree_item_to_object[item_id] = wall
        
        # 添加GLINE对象
        if self.current_model.glines:
            gline_root = self.objects_tree.insert('', 'end', text=f'GLINE ({len(self.current_model.glines)})', 
                                                values=('容器', '几何线段'))
            for i, gline in enumerate(self.current_model.glines):
                details = f"({gline.start_point.x:.1f},{gline.start_point.y:.1f}) -> ({gline.end_point.x:.1f},{gline.end_point.y:.1f})"
                item_id = self.objects_tree.insert(gline_root, 'end', text=f'GLine {i+1}', 
                                                 values=('GLINE', details))
                # 建立树形控件项目到对象的映射
                self.tree_item_to_object[item_id] = gline
        
        # 展开所有节点
        for item in self.objects_tree.get_children():
            self.objects_tree.item(item, open=True)
    
    def _on_object_select(self, event):
        """处理对象列表选择事件"""
        selection = self.objects_tree.selection()
        if not selection:
            # 没有选择任何项目，清除高亮
            self.canvas.clear_selection()
            return
        
        selected_objects = []
        for item_id in selection:
            if item_id in self.tree_item_to_object:
                # 这是一个具体的对象（不是容器节点）
                obj = self.tree_item_to_object[item_id]
                selected_objects.append(obj)
        
        if selected_objects:
            # 高亮选中的对象
            if len(selected_objects) == 1:
                self.canvas.select_object(selected_objects[0])
            else:
                self.canvas.select_objects(selected_objects)
            
            # 更新状态栏
            obj_types = [type(obj).__name__ for obj in selected_objects]
            self.status_label.config(text=f"已选择: {len(selected_objects)}个对象 ({', '.join(set(obj_types))})")
        else:
            # 选择的是容器节点，清除高亮
            self.canvas.clear_selection()
            self.status_label.config(text="就绪")
    
    def clear_selection(self):
        """清除所有选择"""
        # 清除树形控件的选择
        self.objects_tree.selection_remove(self.objects_tree.selection())
        # 清除画布的高亮
        self.canvas.clear_selection()
        # 更新状态栏
        self.status_label.config(text="就绪")
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """ZDEM模型可视化编辑器 v1.0

一个用于可视化和编辑ZDEM模型文件的工具

功能特性:
• 支持WALL和GLINE对象解析
• 第一象限坐标系显示
• 动态缩放和适应
• 对象信息查看
• 对象选择和高亮
"""
        messagebox.showinfo("关于", about_text)
    
    def run(self):
        """运行主循环"""
        self.root.mainloop()