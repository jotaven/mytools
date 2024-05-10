from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('qrcode/', views.generate_qrcode, name='qrcode'),
    path('qrcode/read/', views.read_qrcode, name='read_qrcode'),
    path('ocr/', views.ocr, name='ocr'),
    path('removebg/', views.removebg, name='removebg'),
]
