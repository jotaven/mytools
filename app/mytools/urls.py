from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('qrcode/', views.qrcode, name='qrcode'),
    path('ocr/', views.ocr, name='ocr'),
]
