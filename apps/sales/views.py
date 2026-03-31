"""Sales views."""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Supply, Demand
from .forms import SupplyForm, DemandForm


@login_required
def index(request):
    """销售系统首页。"""
    return render(request, 'sales/index.html')


@login_required
def supply_list(request):
    """供应信息列表。"""
    # 获取筛选参数
    search_query = request.GET.get('q', '')
    spec = request.GET.get('spec', '')
    letter = request.GET.get('letter', '')
    stock_location = request.GET.get('stock_location', '')
    origin = request.GET.get('origin', '')
    price_type = request.GET.get('price_type', '')
    invoice_type = request.GET.get('invoice_type', '')
    standard = request.GET.get('standard', '')
    goods_type = request.GET.get('goods_type', '')
    
    # 构建查询
    query = models.Q()
    
    # 搜索关键词
    if search_query:
        query |= models.Q(medicine_name__icontains=search_query)
    
    # 规格搜索
    if spec:
        query &= models.Q(specification__icontains=spec)
    
    # 字母筛选
    if letter:
        # 筛选药材名称以指定字母开头的记录
        query &= models.Q(medicine_name__istartswith=letter)
    
    # 库存地筛选
    if stock_location:
        query &= models.Q(location__icontains=stock_location)
    
    # 产地筛选
    if origin:
        query &= models.Q(origin__icontains=origin)
    
    # 价格类型筛选
    if price_type == 'quoted':
        query &= models.Q(price__ne='') & ~models.Q(price__icontains='电议')
    elif price_type == 'negotiated':
        query &= models.Q(price__icontains='电议')
    
    # 票据类型筛选
    if invoice_type:
        query &= models.Q(invoice_requirement__icontains=invoice_type)
    
    # 标准筛选
    if standard:
        query &= models.Q(quality_requirement__icontains=standard)
    
    # 货物类型筛选
    if goods_type:
        # 这里需要根据实际数据结构调整
        pass
    
    # 执行查询
    supplies = Supply.objects.filter(query)
    
    # 获取今日价格数据
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')
    today_supplies = Supply.objects.filter(update_time=today).order_by('medicine_name')
    
    # 如果数据库中没有今日价格数据，尝试导入
    if not today_supplies.exists():
        try:
            import import_price_data
            import_price_data.import_price_to_database()
            # 重新获取今日价格数据
            today_supplies = Supply.objects.filter(update_time=today).order_by('medicine_name')
        except Exception as import_error:
            print(f"导入价格数据失败：{import_error}")
    
    # 省份列表
    provinces = [
        '北京市', '天津市', '河北省', '山西省', '内蒙古', '辽宁省', '吉林省', '黑龙江省',
        '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省',
        '湖北省', '湖南省', '广东省', '广西', '海南省', '重庆市', '四川省', '贵州省',
        '云南省', '西藏', '陕西省', '甘肃省', '青海省', '宁夏', '新疆'
    ]
    
    return render(request, 'sales/supply_list.html', {
        'supplies': supplies,
        'today_supplies': today_supplies,
        'today': today,
        'search_query': search_query,
        'spec': spec,
        'letter': letter,
        'stock_location': stock_location,
        'origin': origin,
        'price_type': price_type,
        'invoice_type': invoice_type,
        'standard': standard,
        'goods_type': goods_type,
        'provinces': provinces
    })


@login_required
def demand_list(request):
    """求购信息列表。"""
    # 获取筛选参数
    search_query = request.GET.get('q', '')
    spec = request.GET.get('spec', '')
    letter = request.GET.get('letter', '')
    stock_location = request.GET.get('stock_location', '')
    origin = request.GET.get('origin', '')
    price_type = request.GET.get('price_type', '')
    invoice_type = request.GET.get('invoice_type', '')
    standard = request.GET.get('standard', '')
    goods_type = request.GET.get('goods_type', '')
    
    # 构建查询
    query = models.Q()
    
    # 搜索关键词
    if search_query:
        query |= models.Q(medicine_name__icontains=search_query)
    
    # 规格搜索
    if spec:
        query &= models.Q(specification__icontains=spec)
    
    # 字母筛选
    if letter:
        # 筛选药材名称以指定字母开头的记录
        query &= models.Q(medicine_name__istartswith=letter)
    
    # 库存地筛选
    if stock_location:
        query &= models.Q(location__icontains=stock_location)
    
    # 产地筛选
    if origin:
        query &= models.Q(origin__icontains=origin)
    
    # 价格类型筛选
    if price_type == 'quoted':
        query &= models.Q(price__ne='') & ~models.Q(price__icontains='电议')
    elif price_type == 'negotiated':
        query &= models.Q(price__icontains='电议')
    
    # 票据类型筛选
    if invoice_type:
        query &= models.Q(invoice_requirement__icontains=invoice_type)
    
    # 标准筛选
    if standard:
        query &= models.Q(quality_requirement__icontains=standard)
    
    # 货物类型筛选
    if goods_type:
        # 这里需要根据实际数据结构调整
        pass
    
    # 执行查询
    demands = Demand.objects.filter(query)
    
    # 省份列表
    provinces = [
        '北京市', '天津市', '河北省', '山西省', '内蒙古', '辽宁省', '吉林省', '黑龙江省',
        '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省',
        '湖北省', '湖南省', '广东省', '广西', '海南省', '重庆市', '四川省', '贵州省',
        '云南省', '西藏', '陕西省', '甘肃省', '青海省', '宁夏', '新疆'
    ]
    
    return render(request, 'sales/demand_list.html', {
        'demands': demands,
        'search_query': search_query,
        'spec': spec,
        'letter': letter,
        'stock_location': stock_location,
        'origin': origin,
        'price_type': price_type,
        'invoice_type': invoice_type,
        'standard': standard,
        'goods_type': goods_type,
        'provinces': provinces
    })


@login_required
def supply_detail(request, pk):
    """供应信息详情。"""
    supply = get_object_or_404(Supply, pk=pk)
    
    # 尝试查找对应的中药材信息
    medicine_info = None
    try:
        from apps.medicine.models import Medicine
        medicine_info = Medicine.objects.filter(name=supply.medicine_name).first()
        # 如果找到了，更新supply的medicine字段
        if medicine_info and not supply.medicine:
            supply.medicine = medicine_info
            supply.save()
    except:
        pass
    
    # 获取该商家的其他供应（排除当前记录）
    other_supplies = Supply.objects.filter(
        contact_name=supply.contact_name
    ).exclude(pk=pk)[:10]
    
    # 获取相关供应（同一种药材，排除当前记录和该商家的其他供应）
    related_supplies = Supply.objects.filter(
        medicine_name=supply.medicine_name
    ).exclude(pk=pk).exclude(contact_name=supply.contact_name)[:10]
    
    return render(request, 'sales/supply_detail.html', {
        'supply': supply,
        'medicine_info': medicine_info,
        'other_supplies': other_supplies,
        'related_supplies': related_supplies
    })


@login_required
def demand_detail(request, pk):
    """求购信息详情。"""
    demand = get_object_or_404(Demand, pk=pk)
    
    # 获取该商家的其他求购（排除当前记录）
    other_demands = Demand.objects.filter(
        contact_name=demand.contact_name
    ).exclude(pk=pk)[:10]
    
    # 获取相关求购（同一种药材，排除当前记录和该商家的其他求购）
    related_demands = Demand.objects.filter(
        medicine_name=demand.medicine_name
    ).exclude(pk=pk).exclude(contact_name=demand.contact_name)[:10]
    
    return render(request, 'sales/demand_detail.html', {
        'demand': demand,
        'other_demands': other_demands,
        'related_demands': related_demands
    })


@login_required
def create_supply(request):
    """创建供应信息。"""
    if request.method == 'POST':
        form = SupplyForm(request.POST)
        if form.is_valid():
            supply = form.save(commit=False)
            supply.user = request.user
            supply.save()
            return redirect('sales:supply_list')
    else:
        form = SupplyForm()
    return render(request, 'sales/create_supply.html', {'form': form})


@login_required
def create_demand(request):
    """创建求购信息。"""
    if request.method == 'POST':
        form = DemandForm(request.POST)
        if form.is_valid():
            demand = form.save(commit=False)
            demand.user = request.user
            demand.save()
            return redirect('sales:demand_list')
    else:
        form = DemandForm()
    return render(request, 'sales/create_demand.html', {'form': form})


@login_required
def price_list(request):
    """价格列表，支持分页和搜索。"""
    from django.core.paginator import Paginator
    from datetime import date
    from django.db import models
    
    # 获取搜索关键词
    search_query = request.GET.get('q', '')
    
    # 获取今日价格数据
    today = date.today().strftime('%Y-%m-%d')
    query = models.Q(update_time=today)
    
    # 添加搜索条件
    if search_query:
        query &= models.Q(
            models.Q(medicine_name__icontains=search_query) |
            models.Q(specification__icontains=search_query) |
            models.Q(origin__icontains=search_query)
        )
    
    today_supplies = Supply.objects.filter(query).order_by('medicine_name')
    
    # 检查是否需要加载数据
    need_load_data = not today_supplies.exists()
    
    # 分页处理
    paginator = Paginator(today_supplies, 20)  # 每页20条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 省份列表
    provinces = [
        '北京市', '天津市', '河北省', '山西省', '内蒙古', '辽宁省', '吉林省', '黑龙江省',
        '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省',
        '湖北省', '湖南省', '广东省', '广西', '海南省', '重庆市', '四川省', '贵州省',
        '云南省', '西藏', '陕西省', '甘肃省', '青海省', '宁夏', '新疆'
    ]
    
    return render(request, 'sales/price_list.html', {
        'page_obj': page_obj,
        'today': today,
        'provinces': provinces,
        'search_query': search_query,
        'need_load_data': need_load_data
    })


@login_required
def load_price_data(request):
    """后台加载价格数据。"""
    import json
    from django.http import JsonResponse
    
    try:
        from .utils import import_price_data
        import_price_data.import_price_to_database()
        return JsonResponse({'success': True, 'message': '数据加载成功'})
    except Exception as import_error:
        print(f"导入价格数据失败：{import_error}")
        return JsonResponse({'success': False, 'message': f'数据加载失败：{str(import_error)}'})


@login_required
def update_supply(request, pk):
    """更新供应信息。"""
    supply = get_object_or_404(Supply, pk=pk)
    
    # 检查用户是否有权限修改（只有创建者或超级用户可以修改）
    if supply.user != request.user and not request.user.is_superuser:
        return redirect('sales:supply_detail', pk=pk)
    
    if request.method == 'POST':
        form = SupplyForm(request.POST, instance=supply)
        if form.is_valid():
            form.save()
            return redirect('sales:supply_detail', pk=pk)
    else:
        form = SupplyForm(instance=supply)
    
    return render(request, 'sales/create_supply.html', {'form': form, 'is_update': True})


@login_required
def delete_supply(request, pk):
    """删除供应信息。"""
    supply = get_object_or_404(Supply, pk=pk)
    
    # 检查用户是否有权限删除（只有创建者或超级用户可以删除）
    if supply.user == request.user or request.user.is_superuser:
        supply.delete()
    
    return redirect('account:profile')


@login_required
def update_demand(request, pk):
    """更新求购信息。"""
    demand = get_object_or_404(Demand, pk=pk)
    
    # 检查用户是否有权限修改（只有创建者或超级用户可以修改）
    if demand.user != request.user and not request.user.is_superuser:
        return redirect('sales:demand_detail', pk=pk)
    
    if request.method == 'POST':
        form = DemandForm(request.POST, instance=demand)
        if form.is_valid():
            form.save()
            return redirect('sales:demand_detail', pk=pk)
    else:
        form = DemandForm(instance=demand)
    
    return render(request, 'sales/create_demand.html', {'form': form, 'is_update': True})


@login_required
def delete_demand(request, pk):
    """删除求购信息。"""
    demand = get_object_or_404(Demand, pk=pk)
    
    # 检查用户是否有权限删除（只有创建者或超级用户可以删除）
    if demand.user == request.user or request.user.is_superuser:
        demand.delete()
    
    return redirect('account:profile')


def get_price_history(request):
    """获取价格历史数据。"""
    import json
    from django.http import JsonResponse
    
    medicine_name = request.GET.get('medicine_name')
    specification = request.GET.get('specification')
    origin = request.GET.get('origin')
    market = request.GET.get('market', 'bozhou')  # 默认亳州市场
    
    if not medicine_name or not specification or not origin:
        return JsonResponse({'error': '缺少必要参数'}, status=400)
    
    try:
        from .models import PriceHistory
        
        # 获取价格历史数据
        history = PriceHistory.objects.filter(
            medicine_name=medicine_name,
            specification=specification,
            origin=origin
        ).order_by('date')
        
        # 准备数据
        dates = []
        prices = []
        
        for item in history:
            dates.append(item.date.strftime('%Y-%m-%d'))
            # 根据市场获取价格
            price_field = f'{market}_price'
            price_str = getattr(item, price_field, '无')
            
            # 提取价格数字
            import re
            price_match = re.search(r'\d+(\.\d+)?', str(price_str))
            if price_match:
                prices.append(float(price_match.group()))
            else:
                prices.append(None)
        
        return JsonResponse({
            'dates': dates,
            'prices': prices,
            'medicine_name': medicine_name,
            'specification': specification,
            'origin': origin,
            'market': market
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
