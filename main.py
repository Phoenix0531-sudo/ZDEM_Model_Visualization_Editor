#!/usr/bin/env python3
"""
ZDEM模型可视化编辑器
主程序入口
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zdem_editor.ui.main_window_en import MainWindow


def main():
    """主函数"""
    try:
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()