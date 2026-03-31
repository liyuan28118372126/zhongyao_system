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

from apps.sales.models import Supply, PriceHistory
from apps.medicine.models import Medicine

# 导入爬取模块
from .price_crawler import main as crawl_main
from .price_crawler import get_last_update_info

def import_price_to_database():
    """将爬取的价格数据导入数据库"""
    print("\n===== 开始导入价格数据到数据库 =====")
    
    # 执行爬取
    crawl_main()
    
    # 获取最新爬取的文件路径
    last_info = get_last_update_info()
    save_path = last_info.get('save_path', '')
    
    if not save_path or not os.path.exists(save_path):
        print("❌ 未找到爬取的价格数据文件")
        return
    
    print(f"✅ 找到价格数据文件：{save_path}")
    
    # 从文件名中提取日期
    import re
    date_match = re.search(r'价格_(\d{8})\.xlsx', save_path)
    if date_match:
        file_date = datetime.strptime(date_match.group(1), '%Y%m%d').date()
    else:
        # 如果文件名中没有日期，使用当前日期
        file_date = date.today()
    
    print(f"✅ 提取文件日期：{file_date}")
    
    # 检查是否已经存在该日期的价格历史数据
    existing_history = PriceHistory.objects.filter(date=file_date)
    if existing_history.exists():
        print(f"✅ 日期 {file_date} 的价格历史数据已存在，共 {existing_history.count()} 条记录，跳过导入")
    else:
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
        history_count = 0
        
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
                        'update_time': file_date.strftime('%Y-%m-%d'),
                        'contact_name': '系统',
                        'contact_phone': '12345678900'
                    }
                )
                
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
                    supply.update_time = file_date.strftime('%Y-%m-%d')
                    supply.save()
                    updated_count += 1
                
                # 创建价格历史记录
                history, history_created = PriceHistory.objects.get_or_create(
                    medicine_name=medicine_name,
                    specification=specification,
                    origin=origin,
                    date=file_date,
                    defaults={
                        'bozhou_price': bozhou_price,
                        'angui_price': angui_price,
                        'chengdu_price': chengdu_price,
                        'yulin_price': yulin_price,
                        'lianqiao_price': lianqiao_price,
                        'puning_price': puning_price
                    }
                )
                
                if history_created:
                    history_count += 1
                
            except Exception as e:
                print(f"❌ 处理记录失败（{index+1}）：{e}")
                continue
        
        print(f"\n===== 数据导入完成 =====")
        print(f"- 新增供应记录：{imported_count}")
        print(f"- 更新供应记录：{updated_count}")
        print(f"- 新增价格历史记录：{history_count}")
        print(f"- 总计处理：{imported_count + updated_count}")
    
    # 导入所有历史价格文件
    import_history_price_files()

def get_today_prices():
    """获取今日价格数据"""
    today = date.today().strftime('%Y-%m-%d')
    supplies = Supply.objects.filter(update_time=today).order_by('medicine_name')
    return supplies


def import_history_price_files():
    """导入所有历史价格文件"""
    print("\n===== 开始导入历史价格文件 =====")
    
    # 历史价格文件目录
    history_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "中药价格数据")
    
    if not os.path.exists(history_dir):
        print(f"❌ 历史价格文件目录不存在：{history_dir}")
        return
    
    # 获取目录下的所有Excel文件
    import glob
    excel_files = glob.glob(os.path.join(history_dir, "*.xlsx"))
    
    print(f"✅ 找到 {len(excel_files)} 个历史价格文件")
    
    # 处理每个文件
    total_imported = 0
    
    for file_path in excel_files:
        try:
            # 从文件名中提取日期
            import re
            file_name = os.path.basename(file_path)
            date_match = re.search(r'价格_(\d{8})\.xlsx', file_name)
            if not date_match:
                # 尝试其他日期格式
                date_match = re.search(r'(\d{4})(\d{2})(\d{2})', file_name)
                if date_match:
                    date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
                    file_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                else:
                    print(f"❌ 无法从文件名提取日期：{file_name}")
                    continue
            else:
                file_date = datetime.strptime(date_match.group(1), '%Y%m%d').date()
            
            # 检查是否已经存在该日期的价格历史数据
            existing_history = PriceHistory.objects.filter(date=file_date)
            if existing_history.exists():
                print(f"✅ 日期 {file_date} 的价格历史数据已存在，跳过文件：{file_name}")
                continue
            
            # 读取Excel文件
            df = pd.read_excel(file_path)
            print(f"✅ 读取文件：{file_name}，共 {len(df)} 条记录")
            
            # 处理数据并导入数据库
            file_imported = 0
            
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
                    
                    # 创建价格历史记录
                    history, history_created = PriceHistory.objects.get_or_create(
                        medicine_name=medicine_name,
                        specification=specification,
                        origin=origin,
                        date=file_date,
                        defaults={
                            'bozhou_price': bozhou_price,
                            'angui_price': angui_price,
                            'chengdu_price': chengdu_price,
                            'yulin_price': yulin_price,
                            'lianqiao_price': lianqiao_price,
                            'puning_price': puning_price
                        }
                    )
                    
                    if history_created:
                        file_imported += 1
                        total_imported += 1
                    
                except Exception as e:
                    print(f"❌ 处理文件 {file_name} 中的记录失败（{index+1}）：{e}")
                    continue
            
            print(f"✅ 文件 {file_name} 导入完成，新增 {file_imported} 条历史记录")
            
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 失败：{e}")
            continue
    
    print(f"\n===== 历史价格文件导入完成 =====")
    print(f"- 总计新增历史记录：{total_imported}")


if __name__ == "__main__":
    import_price_to_database()
