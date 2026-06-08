"""
主窗口界面 - 英文版
提供文件操作和模型显示功能，避免中文字体问题
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from typing import Optional

from ..core.parser import ZDEMParser
from ..core.models import ZDEMModel
from .canvas import ZDEMCanvas


class MainWindow:
    """主窗口类 - 英文界面"""
    
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
        self.root.title("ZDEM Model Visualization Editor")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
    
    def _create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_view, accelerator="F5")
        view_menu.add_command(label="Fit Window", command=self.fit_view, accelerator="Ctrl+F")
        view_menu.add_separator()
        view_menu.add_command(label="Clear Selection", command=self.clear_selection, accelerator="Esc")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F5>', lambda e: self.refresh_view())
        self.root.bind('<Control-f>', lambda e: self.fit_view())
        self.root.bind('<Escape>', lambda e: self.clear_selection())
    
    def _create_widgets(self):
        """创建界面组件"""
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        
        # Toolbar
        self.toolbar = ttk.Frame(self.main_frame)
        self.open_btn = ttk.Button(self.toolbar, text="Open File", command=self.open_file)
        self.refresh_btn = ttk.Button(self.toolbar, text="Refresh", command=self.refresh_view)
        
        # Content area - using PanedWindow
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        
        # Left panel - info display
        self.left_panel = ttk.Frame(self.paned_window, width=300)
        self.info_notebook = ttk.Notebook(self.left_panel)
        
        # Model info tab
        self.info_frame = ttk.Frame(self.info_notebook)
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=15, width=35)
        self.info_notebook.add(self.info_frame, text="Model Info")
        
        # Object list tab
        self.objects_frame = ttk.Frame(self.info_notebook)
        self.objects_tree = ttk.Treeview(self.objects_frame, columns=('type', 'details'), show='tree headings')
        self.objects_tree.heading('#0', text='Object')
        self.objects_tree.heading('type', text='Type')
        self.objects_tree.heading('details', text='Details')
        self.objects_scrollbar = ttk.Scrollbar(self.objects_frame, orient=tk.VERTICAL, command=self.objects_tree.yview)
        self.objects_tree.configure(yscrollcommand=self.objects_scrollbar.set)
        
        # Bind object selection event
        self.objects_tree.bind('<<TreeviewSelect>>', self._on_object_select)
        
        self.info_notebook.add(self.objects_frame, text="Object List")
        
        # Right panel - canvas
        self.right_panel = ttk.Frame(self.paned_window)
        self.canvas = ZDEMCanvas(self.right_panel)
        
        # Status bar
        self.status_bar = ttk.Frame(self.main_frame)
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        
        # Add panels to PanedWindow
        self.paned_window.add(self.left_panel, weight=1)
        self.paned_window.add(self.right_panel, weight=3)
    
    def _setup_layout(self):
        """设置布局"""
        # Main frame
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Toolbar
        self.toolbar.pack(fill=tk.X, pady=(0, 5))
        self.open_btn.pack(side=tk.LEFT, padx=(0, 5))
        self.refresh_btn.pack(side=tk.LEFT)
        
        # Content area
        self.paned_window.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Left panel layout
        self.info_notebook.pack(fill=tk.BOTH, expand=True, padx=(0, 5))
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Object list layout
        self.objects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        self.objects_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
        
        # Right panel layout
        self.canvas.get_widget().pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar.pack(fill=tk.X)
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Initialize info display
        self._update_info_display()
    
    def open_file(self):
        """打开文件对话框"""
        file_path = filedialog.askopenfilename(
            title="Select ZDEM File",
            filetypes=[
                ("Python files", "*.py"),
                ("ZDEM files", "*.zdem"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path: str):
        """加载文件"""
        try:
            self.status_label.config(text="Parsing file...")
            self.root.update()
            
            # Parse file
            self.current_model = self.parser.parse_file(file_path)
            self.current_file = file_path
            
            # Update display
            self.canvas.set_model(self.current_model)
            self._update_info_display()
            self._update_objects_tree()
            
            # Update status
            filename = os.path.basename(file_path)
            self.status_label.config(text=f"Loaded: {filename} - {self.current_model.object_count} objects")
            self.root.title(f"ZDEM Model Visualization Editor - {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            self.status_label.config(text="Load failed")
    
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
                info = f"File: {os.path.basename(self.current_file)}\n\n" + info
            
            # Add boundary info
            bounds = self.current_model.bounds
            info += f"\n\nBoundary Info:"
            info += f"\n  X Range: {bounds[0]:.2f} ~ {bounds[2]:.2f}"
            info += f"\n  Y Range: {bounds[1]:.2f} ~ {bounds[3]:.2f}"
            info += f"\n  Width: {bounds[2] - bounds[0]:.2f}"
            info += f"\n  Height: {bounds[3] - bounds[1]:.2f}"
            
        else:
            info = "No model file loaded\n\nPlease use File -> Open File to load a ZDEM model"
        
        self.info_text.insert(1.0, info)
    
    def _update_objects_tree(self):
        """更新对象列表"""
        # Clear existing items and mapping
        for item in self.objects_tree.get_children():
            self.objects_tree.delete(item)
        self.tree_item_to_object.clear()
        
        if not self.current_model:
            return
        
        # Add WALL objects
        if self.current_model.walls:
            wall_root = self.objects_tree.insert('', 'end', text=f'WALL ({len(self.current_model.walls)})', 
                                               values=('Container', 'Wall Objects'))
            for i, wall in enumerate(self.current_model.walls):
                details = f"({wall.start_point.x:.1f},{wall.start_point.y:.1f}) -> ({wall.end_point.x:.1f},{wall.end_point.y:.1f})"
                item_id = self.objects_tree.insert(wall_root, 'end', text=f'Wall {wall.id or i+1}', 
                                                 values=('WALL', details))
                # Build mapping from tree item to object
                self.tree_item_to_object[item_id] = wall
        
        # Add GLINE objects
        if self.current_model.glines:
            gline_root = self.objects_tree.insert('', 'end', text=f'GLINE ({len(self.current_model.glines)})', 
                                                values=('Container', 'Geometry Lines'))
            for i, gline in enumerate(self.current_model.glines):
                details = f"({gline.start_point.x:.1f},{gline.start_point.y:.1f}) -> ({gline.end_point.x:.1f},{gline.end_point.y:.1f})"
                item_id = self.objects_tree.insert(gline_root, 'end', text=f'GLine {i+1}', 
                                                 values=('GLINE', details))
                # Build mapping from tree item to object
                self.tree_item_to_object[item_id] = gline
        
        # Add PROP P4 objects
        if self.current_model.prop_p4s:
            prop_p4_root = self.objects_tree.insert('', 'end', text=f'PROP P4 ({len(self.current_model.prop_p4s)})', 
                                                   values=('Container', 'P4 Polygons'))
            for i, prop_p4 in enumerate(self.current_model.prop_p4s):
                # Display polygon boundary info
                bounds = prop_p4.bounds
                details = f"Bounds: ({bounds[0]:.1f},{bounds[1]:.1f}) - ({bounds[2]:.1f},{bounds[3]:.1f})"
                item_id = self.objects_tree.insert(prop_p4_root, 'end', text=f'P4 {i+1}', 
                                                 values=('PROP P4', details))
                # Build mapping from tree item to object
                self.tree_item_to_object[item_id] = prop_p4
        
        # Expand all nodes
        for item in self.objects_tree.get_children():
            self.objects_tree.item(item, open=True)
    
    def _on_object_select(self, event):
        """处理对象列表选择事件"""
        selection = self.objects_tree.selection()
        if not selection:
            # No selection, clear highlight
            self.canvas.clear_selection()
            return
        
        selected_objects = []
        for item_id in selection:
            if item_id in self.tree_item_to_object:
                # This is a specific object (not container node)
                obj = self.tree_item_to_object[item_id]
                selected_objects.append(obj)
        
        if selected_objects:
            # Highlight selected objects
            if len(selected_objects) == 1:
                self.canvas.select_object(selected_objects[0])
            else:
                self.canvas.select_objects(selected_objects)
            
            # Update status bar
            obj_types = [type(obj).__name__ for obj in selected_objects]
            self.status_label.config(text=f"Selected: {len(selected_objects)} objects ({', '.join(set(obj_types))})")
        else:
            # Selected container node, clear highlight
            self.canvas.clear_selection()
            self.status_label.config(text="Ready")
    
    def clear_selection(self):
        """清除所有选择"""
        # Clear tree selection
        self.objects_tree.selection_remove(self.objects_tree.selection())
        # Clear canvas highlight
        self.canvas.clear_selection()
        # Update status bar
        self.status_label.config(text="Ready")
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """ZDEM Model Visualization Editor v1.0

A tool for visualizing and editing ZDEM model files

Features:
• Support for WALL and GLINE object parsing
• First quadrant coordinate system display
• Dynamic scaling and fitting
• Object information viewing
• Object selection and highlighting
"""
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """运行主循环"""
        self.root.mainloop()