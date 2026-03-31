#!/usr/bin/env python3
"""导入中药材供应和求购信息到数据库。"""

import os
import sys
import pandas as pd

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyao_system.settings')

import django
django.setup()

from apps.sales.models import Supply, Demand


def import_supply_data():
    """导入中药材供应信息。"""
    file_path = os.path.join('static', 'data', '中药材供应信息.xlsx')
    
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    # 读取Excel文件
    df = pd.read_excel(file_path)
    
    # 打印列名
    print("供应信息列名:", df.columns.tolist())
    
    # 导入数据
    imported_count = 0
    for index, row in df.iterrows():
        # 处理空值的函数
        def process_value(value):
            if value is None:
                return ''
            if isinstance(value, float) and pd.isna(value):
                return ''
            if str(value).strip() in ['未填写', 'nan', 'NaN', 'NAN']:
                return ''
            return str(value).strip()
        
        # 获取数据
        medicine_name = process_value(row.get('药材名称'))
        
        if not medicine_name:
            continue
        
        specification = process_value(row.get('规格'))
        quantity = process_value(row.get('供应数量'))
        location = process_value(row.get('药材库存地'))  # 药材库存地
        origin = process_value(row.get('药材产地'))  # 药材产地
        invoice_requirement = process_value(row.get('票据需求'))  # 票据需求
        quality_requirement = process_value(row.get('质量需求'))  # 质量需求
        qualification_requirement = process_value(row.get('资质要求'))  # 资质要求
        sample = process_value(row.get('寄样'))  # 寄样
        payment = process_value(row.get('付款'))  # 付款
        packaging = process_value(row.get('包装'))  # 包装
        contact_phone = process_value(row.get('联系电话'))  # 联系电话
        contact_name = process_value(row.get('联系人'))  # 联系人
        update_time = process_value(row.get('更新时间'))  # 更新时间
        price = process_value(row.get('售价'))  # 售价
        minimum_order = process_value(row.get('起售量'))  # 起售量
        
        # 创建供应信息
        supply = Supply.objects.create(
            medicine_name=medicine_name,
            specification=specification,
            quantity=quantity,
            location=location,
            origin=origin,
            invoice_requirement=invoice_requirement,
            quality_requirement=quality_requirement,
            qualification_requirement=qualification_requirement,
            sample=sample,
            payment=payment,
            packaging=packaging,
            contact_phone=contact_phone,
            contact_name=contact_name,
            update_time=update_time,
            price=price,
            minimum_order=minimum_order,
            description=specification  # 描述也使用规格数据
        )
        
        print(f"创建供应信息: {medicine_name}, 价格: {price}, 数量: {quantity}")
        imported_count += 1
    
    print(f"供应信息导入完成，共导入 {imported_count} 条数据")

def import_demand_data():
    """导入中药材求购信息。"""
    file_path = os.path.join('static', 'data', '中药材求购信息.xlsx')
    
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    # 读取Excel文件
    df = pd.read_excel(file_path)
    
    # 打印列名
    print("求购信息列名:", df.columns.tolist())
    
    # 导入数据
    imported_count = 0
    for index, row in df.iterrows():
        # 获取数据
        medicine_name = str(row.get('药材名称', '')).strip()
        
        if not medicine_name:
            continue
        
        specification = str(row.get('规格', '')).strip()
        quantity = str(row.get('供应数量', '')).strip()
        location = str(row.get('药材库存地', '')).strip()
        origin = str(row.get('药材产地', '')).strip()
        price = str(row.get('售价', '')).strip()
        contact_name = str(row.get('联系人', '')).strip()
        contact_phone = str(row.get('联系电话', '')).strip()
        update_time = str(row.get('更新时间', '')).strip()
        
        # 创建求购信息
        demand = Demand.objects.create(
            medicine_name=medicine_name,
            specification=specification,
            quantity=quantity,
            location=location,
            origin=origin,
            price=price,
            contact_name=contact_name,
            contact_phone=contact_phone,
            update_time=update_time,
            description=specification
        )
        
        print(f"创建求购信息: {medicine_name}, 价格: {price}, 数量: {quantity}")
        imported_count += 1
    
    print(f"求购信息导入完成，共导入 {imported_count} 条数据")


if __name__ == '__main__':
    print("开始导入中药材销售数据...")
    import_supply_data()
    print("\n" + "="*50 + "\n")
    import_demand_data()
    print("\n数据导入完成！")
