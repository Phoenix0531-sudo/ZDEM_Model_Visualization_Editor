#!/usr/bin/env python3
"""
测试PROP P4四边形功能
"""

from zdem_editor.core.parser import ZDEMParser
import tempfile
import os

def test_prop_p4_parsing():
    """测试PROP P4四边形解析功能"""
    
    # 测试用例 - 基于实际文件中的PROP P4语法
    test_cases = [
        # 标准PROP P4格式
        "prop group presturct range P4 (10500.0, 12125.0) (10600.0, 12225.0) (19980.0, 14375.0) (19980.0, 14475.0)",
        
        # 另一个PROP P4格式
        "prop group presturct range P4 (19980.0, 14375.0) (20080.0, 14475.0) (29080.0, 15375.0) (29180.0, 15475.0)",
        
        # 带颜色的PROP P4
        "prop color red range P4 (0.0, 0.0) (100.0, 0.0) (100.0, 100.0) (0.0, 100.0)",
        
        # 简化格式
        "PROP GROUP test RANGE P4 (1.0, 1.0) (2.0, 1.0) (2.0, 2.0) (1.0, 2.0)",
    ]
    
    print("🔍 测试PROP P4四边形解析功能")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"输入: {test_case}")
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.zdem', delete=False) as f:
            f.write(test_case)
            temp_file = f.name
        
        try:
            # 解析测试
            parser = ZDEMParser()
            model = parser.parse_file(temp_file)
            
            if model.prop_p4s:
                prop_p4 = model.prop_p4s[0]
                print(f"✅ 解析成功 (PROP P4):")
                print(f"   组: {prop_p4.group}")
                print(f"   颜色: {prop_p4.color}")
                print(f"   属性类型: {prop_p4.property_type}")
                print(f"   属性值: {prop_p4.property_value}")
                print(f"   顶点数: {len(prop_p4.points)}")
                print(f"   边界: {prop_p4.bounds}")
                
                # 显示所有顶点
                for j, point in enumerate(prop_p4.points):
                    print(f"   顶点{j+1}: ({point.x}, {point.y})")
                    
            else:
                print("❌ 解析失败: 没有找到PROP P4对象")
                if parser.errors:
                    for error in parser.errors:
                        print(f"   错误: {error}")
        
        except Exception as e:
            print(f"❌ 解析异常: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # 清理临时文件
            os.unlink(temp_file)
    
    print("\n" + "=" * 60)
    print("PROP P4解析测试完成")

def test_real_file_with_prop_p4():
    """测试包含PROP P4的实际文件"""
    print("\n🔍 测试包含PROP P4的实际文件")
    print("=" * 60)
    
    test_file = 'Test/shear1.py'
    
    if not os.path.exists(test_file):
        print(f"⚠️  文件不存在: {test_file}")
        return
        
    print(f"\n测试文件: {test_file}")
    
    try:
        parser = ZDEMParser()
        model = parser.parse_file(test_file)
        
        print(f"✅ 解析成功:")
        print(f"   WALL对象: {len(model.walls)}个")
        print(f"   GLINE对象: {len(model.glines)}个")
        print(f"   PROP P4对象: {len(model.prop_p4s)}个")
        print(f"   总计: {model.object_count}个对象")
        
        if parser.errors:
            print(f"   错误: {len(parser.errors)}个")
            for error in parser.errors[:3]:  # 只显示前3个错误
                print(f"     {error}")
            if len(parser.errors) > 3:
                print(f"     ... 还有{len(parser.errors) - 3}个错误")
        
        # 显示PROP P4对象详情
        if model.prop_p4s:
            print(f"\n   PROP P4对象详情:")
            for i, prop_p4 in enumerate(model.prop_p4s):
                print(f"   P4 {i+1}: 组={prop_p4.group}, 颜色={prop_p4.color}, 边界={prop_p4.bounds}")
                
    except Exception as e:
        print(f"❌ 解析失败: {e}")

def test_canvas_integration():
    """测试画布集成"""
    print("\n🔍 测试画布集成")
    print("=" * 60)
    
    try:
        from zdem_editor.ui.canvas import ZDEMCanvas
        import tkinter as tk
        
        # 创建测试模型
        test_content = '''
WALL nodes ( 0.0, 0.0 ) ( 100.0, 0.0 ) kn=1.0 ks=1.0 fric=0.1
GLINE P1 ( 0.0, 0.0 ) P2 ( 0.0, 100.0 ) r 10.0 color blue
prop group test range P4 (20.0, 20.0) (80.0, 20.0) (80.0, 80.0) (20.0, 80.0)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.zdem', delete=False) as f:
            f.write(test_content)
            temp_file = f.name
        
        # 解析模型
        parser = ZDEMParser()
        model = parser.parse_file(temp_file)
        
        # 创建画布测试
        root = tk.Tk()
        root.withdraw()
        canvas = ZDEMCanvas(root)
        canvas.set_model(model)
        
        print(f"✅ 画布集成成功:")
        print(f"   模型对象: {model.object_count}个")
        print(f"   包含: {len(model.walls)}个WALL, {len(model.glines)}个GLINE, {len(model.prop_p4s)}个PROP P4")
        
        # 测试对象选择
        if model.prop_p4s:
            canvas.select_object(model.prop_p4s[0])
            print(f"   P4对象选择测试: 成功")
        
        canvas.clear_selection()
        print(f"   清除选择测试: 成功")
        
        root.destroy()
        os.unlink(temp_file)
        
    except Exception as e:
        print(f"❌ 画布集成失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prop_p4_parsing()
    test_real_file_with_prop_p4()
    test_canvas_integration()