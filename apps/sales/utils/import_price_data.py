import os
import sys
import django
from datetime import date, datetime
import pandas as pd

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django settings模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyao_system.settings')

# 初始化Django
django.setup()

from apps.sales.models import Supply
from apps.medicine.models import Medicine

# 导入爬取模块
from .price_crawler import main as crawl_main
from .price_crawler import get_last_update_info

def import_price_to_database():
    """将爬取的价格数据导入数据库"""
    print("\n===== 开始导入价格数据到数据库 =====")
    
    # 检查是否已经存在今日的价格数据
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')
    existing_supplies = Supply.objects.filter(update_time=today)
    
    if existing_supplies.exists():
        print(f"✅ 今日（{today}）价格数据已存在，共 {existing_supplies.count()} 条记录，跳过爬取")
        return
    
    # 执行爬取
    crawl_main()
    
    # 获取最新爬取的文件路径
    last_info = get_last_update_info()
    save_path = last_info.get('save_path', '')
    
    if not save_path or not os.path.exists(save_path):
        print("❌ 未找到爬取的价格数据文件")
        return
    
    print(f"✅ 找到价格数据文件：{save_path}")
    
    # 读取Excel文件
    try:
        df = pd.read_excel(save_path)
        print(f"✅ 成功读取数据，共 {len(df)} 条记录")
    except Exception as e:
        print(f"❌ 读取Excel文件失败：{e}")
        return
    
    # 处理数据并导入数据库
    imported_count = 0
    updated_count = 0
    
    for index, row in df.iterrows():
        try:
            medicine_name = row.get('品名', '').strip()
            specification = row.get('规格', '').strip()
            origin = row.get('产地', '').strip()
            
            # 提取各个市场的价格
            bozhou_price = row.get('亳州价格', '无')
            angui_price = row.get('安国价格', '无')
            chengdu_price = row.get('成都价格', '无')
            yulin_price = row.get('玉林价格', '无')
            lianqiao_price = row.get('廉桥价格', '无')
            puning_price = row.get('普宁价格', '无')
            
            # 计算平均价格（取所有市场的价格）
            prices = []
            market_prices = [bozhou_price, angui_price, chengdu_price, yulin_price, lianqiao_price, puning_price]
            for price in market_prices:
                if price and price != '无' and price != '--':
                    # 提取价格数字
                    import re
                    price_match = re.search(r'\d+(\.\d+)?', str(price))
                    if price_match:
                        prices.append(float(price_match.group()))
            
            if prices:
                avg_price = sum(prices) / len(prices)
                price_str = f"{avg_price:.2f}元"
            else:
                price_str = "电议"
            
            # 查找或创建供应记录
            supply, created = Supply.objects.get_or_create(
                medicine_name=medicine_name,
                specification=specification,
                origin=origin,
                defaults={
                    'quantity': '大量',
                    'location': origin,
                    'price': price_str,
                    'bozhou_price': bozhou_price,
                    'angui_price': angui_price,
                    'chengdu_price': chengdu_price,
                    'yulin_price': yulin_price,
                    'lianqiao_price': lianqiao_price,
                    'puning_price': puning_price,
                    'update_time': date.today().strftime('%Y-%m-%d'),
                    'contact_name': '系统',
                    'contact_phone': '12345678900'
                }
            )
            
            # 移除保存历史价格记录的代码
            
            if created:
                imported_count += 1
            else:
                # 更新现有记录的价格
                supply.price = price_str
                supply.bozhou_price = bozhou_price
                supply.angui_price = angui_price
                supply.chengdu_price = chengdu_price
                supply.yulin_price = yulin_price
                supply.lianqiao_price = lianqiao_price
                supply.puning_price = puning_price
                supply.update_time = date.today().strftime('%Y-%m-%d')
                supply.save()
                updated_count += 1
            
        except Exception as e:
            print(f"❌ 处理记录失败（{index+1}）：{e}")
            continue
    
    print(f"\n===== 数据导入完成 =====")
    print(f"- 新增记录：{imported_count}")
    print(f"- 更新记录：{updated_count}")
    print(f"- 总计处理：{imported_count + updated_count}")

def get_today_prices():
    """获取今日价格数据"""
    today = date.today().strftime('%Y-%m-%d')
    supplies = Supply.objects.filter(update_time=today).order_by('medicine_name')
    return supplies

if __name__ == "__main__":
    import_price_to_database()
