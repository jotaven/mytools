from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download_image/', views.download_image, name='download_image'),
    path('qrcode/', views.generate_qrcode, name='qrcode'),
    path('qrcode/read/', views.image_read_qrcode, name='read_qrcode'),
    path('ocr/', views.image_ocr, name='ocr'),
    path('removebg/', views.image_removebg, name='removebg'),
    path('contour/', views.image_contour, name='contour'),
    path('scketch/', views.image_scketch, name='scketch'),
]
