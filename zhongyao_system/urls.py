"""Zhongyao System URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('medicine:index')),
    path('admin/', admin.site.urls),
    path('account/', include('apps.account.urls')),
    path('medicine/', include('apps.medicine.urls')),
    path('image-recognition/', include('apps.image_recognition.urls')),
    path('sales/', include('apps.sales.urls')),
    path('news/', include('apps.news.urls')),
    path('llm-qa/', include('apps.llm_qa.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
