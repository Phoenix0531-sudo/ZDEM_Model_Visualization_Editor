#!/usr/bin/env python3
"""
测试增强后的解析器鲁棒性
验证P1/P2格式、数字颜色等新特性
"""

from zdem_editor.core.parser import ZDEMParser
import tempfile
import os

def test_enhanced_parser():
    """测试增强后的解析器功能"""
    
    # 测试用例 - 基于实际文件中的语法
    test_cases = [
        # P1/P2格式的GLINE
        "GLINE P1 (  10000.0,  10000.0 ) P2 (  10000.0, 30000.0 ) r 80.0 color blue GROUP bom_wall",
        
        # 数字颜色的WALL
        "WALL id 0 nodes ( 1000.0, 14250.0 )   ( 1000.0, 18500.0 ) kn=2e3 ks=2e3 fric=0.00 color=1",
        
        # 混合格式
        "GLINE P1 (   100.0,  10000.0 ) P2 (  18500.0, 10000.0 ) r 80.0 color blue GROUP bom_wall",
        
        # 传统格式（确保向后兼容）
        "WALL nodes (  30000.0,  10000.0 ) (  30000.0, 30000.0 ) kn= 11.2e9 ks=11.2e9 fric 0.00 GROUP fault",
        
        # 简化颜色格式
        "GLINE P1 ( 18500.0,  10000.0 ) P2 (  18500.0, 30000.0 ) r 80.0 color blue GROUP right_wall",
        
        # 特殊颜色名称
        "GLINE P1 ( 0.0, 0.0 ) P2 ( 100.0, 100.0 ) r 10.0 color mg GROUP test1",
        "GLINE P1 ( 0.0, 0.0 ) P2 ( 100.0, 100.0 ) r 10.0 color lg GROUP test2",
    ]
    
    print("🔍 测试增强后的解析器鲁棒性")
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
            
            if model.walls:
                obj = model.walls[0]
                obj_type = "WALL"
            elif model.glines:
                obj = model.glines[0]
                obj_type = "GLINE"
            else:
                print("❌ 解析失败: 没有找到对象")
                continue
            
            print(f"✅ 解析成功 ({obj_type}):")
            print(f"   ID: {getattr(obj, 'id', 'N/A')}")
            print(f"   起点: ({obj.start_point.x}, {obj.start_point.y})")
            print(f"   终点: ({obj.end_point.x}, {obj.end_point.y})")
            
            if hasattr(obj, 'radius'):
                print(f"   半径: {obj.radius}")
            
            print(f"   KN: {obj.kn}")
            print(f"   KS: {obj.ks}")
            print(f"   FRIC: {obj.fric}")
            print(f"   颜色: {obj.color}")
            print(f"   组: {obj.group}")
            
            if parser.errors:
                print(f"   警告: {len(parser.errors)}个")
                for error in parser.errors:
                    print(f"     {error}")
        
        except Exception as e:
            print(f"❌ 解析异常: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # 清理临时文件
            os.unlink(temp_file)
    
    print("\n" + "=" * 60)
    print("增强解析器测试完成")

def test_real_files():
    """测试实际文件的解析"""
    print("\n🔍 测试实际文件解析")
    print("=" * 60)
    
    test_files = ['Test/gen0.py', 'Test/shear0.py', 'Test/shear1.py']
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"⚠️  文件不存在: {file_path}")
            continue
            
        print(f"\n测试文件: {file_path}")
        
        try:
            parser = ZDEMParser()
            model = parser.parse_file(file_path)
            
            print(f"✅ 解析成功:")
            print(f"   WALL对象: {len(model.walls)}个")
            print(f"   GLINE对象: {len(model.glines)}个")
            print(f"   总计: {model.object_count}个对象")
            
            if parser.errors:
                print(f"   错误: {len(parser.errors)}个")
                for error in parser.errors[:3]:  # 只显示前3个错误
                    print(f"     {error}")
                if len(parser.errors) > 3:
                    print(f"     ... 还有{len(parser.errors) - 3}个错误")
            
            # 显示一些对象详情
            if model.walls:
                wall = model.walls[0]
                print(f"   示例WALL: ID={wall.id}, 颜色={wall.color}, 组={wall.group}")
            
            if model.glines:
                gline = model.glines[0]
                print(f"   示例GLINE: 半径={gline.radius}, 颜色={gline.color}, 组={gline.group}")
                
        except Exception as e:
            print(f"❌ 解析失败: {e}")

if __name__ == "__main__":
    test_enhanced_parser()
    test_real_files()