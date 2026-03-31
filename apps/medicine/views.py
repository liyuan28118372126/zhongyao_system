"""Medicine views."""

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Medicine, Prescription, DietaryTherapy, AcupuncturePoint


def index(request):
    """Medicine index view."""
    try:
        # Get featured medicines (latest 6)
        featured_medicines = Medicine.objects.all()[:6]
        
        # Get featured prescriptions (latest 4)
        featured_prescriptions = Prescription.objects.all()[:4]
        
        # Get latest news (empty for now)
        latest_news = []
        
        # Get today's prices
        from datetime import date
        from apps.sales.models import Supply
        today = date.today().strftime('%Y-%m-%d')
        
        # 优先从数据库获取今日价格数据
        today_prices = Supply.objects.filter(update_time=today).order_by('medicine_name')
        
        # 检查是否需要加载数据
        need_load_data = not today_prices.exists()
        
        context = {
            'featured_medicines': featured_medicines,
            'featured_prescriptions': featured_prescriptions,
            'latest_news': latest_news,
            'today_prices': today_prices,
            'today': today,
            'need_load_data': need_load_data,
        }
        return render(request, 'medicine/index.html', context)
    except Exception as e:
        # Return error message for debugging
        return render(request, 'medicine/test.html', {'error': str(e)})


def search(request):
    """Search view."""
    query = request.GET.get('q', '')
    
    if query:
        # Search in medicines
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) | 
            Q(functions__icontains=query) |
            Q(indications__icontains=query)
        )
        
        # Search in prescriptions
        prescriptions = Prescription.objects.filter(
            Q(name__icontains=query) | 
            Q(functions__icontains=query) |
            Q(indications__icontains=query)
        )
        
        # Search in dietary therapies
        dietary_therapies = DietaryTherapy.objects.filter(
            Q(name__icontains=query) | 
            Q(functions__icontains=query)
        )
        
        # Search in acupuncture points
        acupuncture_points = AcupuncturePoint.objects.filter(
            Q(name__icontains=query) | 
            Q(functions__icontains=query)
        )
    else:
        medicines = Medicine.objects.none()
        prescriptions = Prescription.objects.none()
        dietary_therapies = DietaryTherapy.objects.none()
        acupuncture_points = AcupuncturePoint.objects.none()
    
    context = {
        'query': query,
        'medicines': medicines,
        'prescriptions': prescriptions,
        'dietary_therapies': dietary_therapies,
        'acupuncture_points': acupuncture_points,
    }
    return render(request, 'medicine/search_results.html', context)


def medicine_list(request):
    """Medicine list view with search functionality."""
    query = request.GET.get('q', '')
    
    if query:
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) | 
            Q(latin_name__icontains=query) |
            Q(functions__icontains=query) |
            Q(indications__icontains=query)
        )
    else:
        medicines = Medicine.objects.all()
    
    context = {
        'medicines': medicines,
        'query': query
    }
    return render(request, 'medicine/medicine_list.html', context)


def medicine_autocomplete(request):
    """Medicine autocomplete view."""
    query = request.GET.get('term', '')
    if query:
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) | 
            Q(latin_name__icontains=query)
        )[:10]
        results = [{'label': medicine.name, 'value': medicine.name} for medicine in medicines]
    else:
        results = []
    
    return JsonResponse(results, safe=False)


def prescription_autocomplete(request):
    """Prescription autocomplete view."""
    query = request.GET.get('term', '')
    if query:
        prescriptions = Prescription.objects.filter(
            Q(name__icontains=query)
        )[:10]
        results = [{'label': prescription.name, 'value': prescription.name} for prescription in prescriptions]
    else:
        results = []
    
    return JsonResponse(results, safe=False)


def dietary_therapy_autocomplete(request):
    """Dietary therapy autocomplete view."""
    query = request.GET.get('term', '')
    if query:
        therapies = DietaryTherapy.objects.filter(
            Q(name__icontains=query)
        )[:10]
        results = [{'label': therapy.name, 'value': therapy.name} for therapy in therapies]
    else:
        results = []
    
    return JsonResponse(results, safe=False)


def acupuncture_point_autocomplete(request):
    """Acupuncture point autocomplete view."""
    query = request.GET.get('term', '')
    if query:
        points = AcupuncturePoint.objects.filter(
            Q(name__icontains=query)
        )[:10]
        results = [{'label': point.name, 'value': point.name} for point in points]
    else:
        results = []
    
    return JsonResponse(results, safe=False)


def medicine_detail(request, pk):
    """Medicine detail view."""
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'medicine/medicine_detail.html', {'medicine': medicine})


def prescription_list(request):
    """Prescription list view with search functionality."""
    query = request.GET.get('q', '')
    
    if query:
        prescriptions = Prescription.objects.filter(
            Q(name__icontains=query) | 
            Q(ingredients__icontains=query) |
            Q(functions__icontains=query) |
            Q(indications__icontains=query)
        )
    else:
        prescriptions = Prescription.objects.all()
    
    context = {
        'prescriptions': prescriptions,
        'query': query
    }
    return render(request, 'medicine/prescription_list.html', context)


def prescription_detail(request, pk):
    """Prescription detail view."""
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'medicine/prescription_detail.html', {'prescription': prescription})


def dietary_therapy_list(request):
    """Dietary therapy list view with search functionality."""
    query = request.GET.get('q', '')
    
    if query:
        dietary_therapies = DietaryTherapy.objects.filter(
            Q(name__icontains=query) | 
            Q(ingredients__icontains=query) |
            Q(functions__icontains=query) |
            Q(indications__icontains=query)
        )
    else:
        dietary_therapies = DietaryTherapy.objects.all()
    
    context = {
        'dietary_therapies': dietary_therapies,
        'query': query
    }
    return render(request, 'medicine/dietary_therapy_list.html', context)


def dietary_therapy_detail(request, pk):
    """Dietary therapy detail view."""
    dietary_therapy = get_object_or_404(DietaryTherapy, pk=pk)
    return render(request, 'medicine/dietary_therapy_detail.html', {'dietary_therapy': dietary_therapy})


def acupuncture_point_list(request):
    """Acupuncture point list view with search functionality."""
    query = request.GET.get('q', '')
    
    if query:
        acupuncture_points = AcupuncturePoint.objects.filter(
            Q(name__icontains=query) | 
            Q(location__icontains=query) |
            Q(functions__icontains=query) |
            Q(indications__icontains=query)
        )
    else:
        acupuncture_points = AcupuncturePoint.objects.all()
    
    context = {
        'acupuncture_points': acupuncture_points,
        'query': query
    }
    return render(request, 'medicine/acupuncture_point_list.html', context)


def acupuncture_point_detail(request, pk):
    """Acupuncture point detail view."""
    acupuncture_point = get_object_or_404(AcupuncturePoint, pk=pk)
    return render(request, 'medicine/acupuncture_point_detail.html', {'acupuncture_point': acupuncture_point})
