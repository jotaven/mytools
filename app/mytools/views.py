from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .forms import ContextForm
from .models import Context

import base64
import requests
import pytesseract
import cv2
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

TESSDATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data/tessdata')
API_URL = os.environ.get('API_URL') if os.environ.get('API_URL') else 'http://api:8001'


def index(request):
    return render(request, 'mytools/index.html')

def generate_qrcode(request):
    if request.method == 'POST':
        print(API_URL)
        if 'text' not in request.POST:
            return render(request, 'mytools/qrcode.html', {'error': 'URL não providenciada!'})
        text = request.POST.get('text')
        response = requests.get(f'{API_URL}/qrcode', params={'url': text})
        if response.status_code == 200:
            imagem = base64.b64encode(response.content).decode('utf-8')
            return render(request, 'mytools/qrcode.html', {'imagem': imagem, 'text': text})
        else:
            return render(request, 'mytools/qrcode.html', {'error': 'Falha ao gerar QrCode!'})

    return render(request, 'mytools/qrcode.html')

def image_ocr(request):
    if request.method == 'POST':
        if 'file_upload' not in request.FILES:
            print(request.FILES)
            return render(request, 'mytools/ocr.html', {'error': 'Imagem não providenciada!'})
        image = cv2.imdecode(np.fromstring(request.FILES['file_upload'].read(), np.uint8), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        resultado = pytesseract.image_to_data(image, lang="por", config=f"--tessdata-dir '{TESSDATA_DIR}'", output_type=pytesseract.Output.DICT)
        resultado = [resultado['text'][i] for i in range(len(resultado['text'])) if resultado['text'][i] != '' and resultado['conf'][i] > 45]
        resultado = ' '.join(resultado)
        return render(request, 'mytools/ocr.html', {'image_text': resultado})

    return render(request, 'mytools/ocr.html')

def image_read_qrcode(request):
    if request.method == 'POST':
        if 'file_upload' not in request.FILES:
            print(request.FILES)
            return render(request, 'mytools/read_qrcode.html', {'error': 'Imagem não providenciada!'})
        extension = request.FILES['file_upload'].name.split('.')[-1]
        if extension not in ['jpg', 'jpeg', 'png']:
            return render(request, 'mytools/read_qrcode.html', {'error': f'Formato {extension} não suportado!'})
        
        qrcdetector = cv2.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode =  qrcdetector.detectAndDecodeMulti(image)
        if not retval:
            image = cv2.imdecode(np.fromstring(request.FILES['file_upload'].read(), np.uint8), cv2.IMREAD_COLOR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.GaussianBlur(image, (5, 5), 0)
            image = cv2.equalizeHist(image)
            
            retval, decoded_info, points, straight_qrcode =  qrcdetector.detectAndDecodeMulti(image)
        
        if points is not None:
            return render(request, 'mytools/read_qrcode.html', {'image_text': decoded_info[0]})
        
        return render(request, 'mytools/read_qrcode.html', {'error': 'Nenhum QR Code encontrado!'})

    return render(request, 'mytools/read_qrcode.html')

        
def image_removebg(request):
    if request.method == "POST" and request.FILES['file_upload']:
        image = request.FILES['file_upload']
        response = requests.post(f'{API_URL}/removebg', files={'image': image})
        if response.status_code == 200:
            imagem = base64.b64encode(response.content).decode('utf-8')
            return render(request, 'mytools/removebg.html', {'imagem': imagem})
        else:
            return render(request, 'mytools/removebg.html', {'error': f'Erro {response.status_code}. Tente novamente mais tarde!'})

    return render(request, 'mytools/removebg.html')

def image_contour(request):
    if request.method == "POST" and request.FILES['file_upload']:
        image = request.FILES['file_upload']
        image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 30, 150)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blank_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        image = cv2.drawContours(blank_image, contours, -1, (0, 255, 0), 3)
        _, img_encoded = cv2.imencode('.png', image)
        img_encoded = base64.b64encode(img_encoded).decode('utf-8')
        return render(request, 'mytools/contour.html', {'imagem': img_encoded})
    return render(request, 'mytools/contour.html')

def image_scketch(request):
    if request.method == "POST" and request.FILES['file_upload']:
        image = request.FILES['file_upload']
        image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (21, 21), 0)
        image = cv2.divide(gray, gray_blur, scale=256)
        _, img_encoded = cv2.imencode('.png', image)
        img_encoded = base64.b64encode(img_encoded).decode('utf-8')
        return render(request, 'mytools/scketch.html', {'imagem': img_encoded})
    return render(request, 'mytools/scketch.html')

def download_image(request):
    if request.method == "POST" and 'imagem' in request.POST:
        imagem = base64.b64decode(request.POST.get('imagem'))
        response = HttpResponse(imagem, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
        return response

def context(request):
    if request.method == 'POST':
        form = ContextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            expires_at = form.cleaned_data['expires_at']
            newContext = Context.objects.create(text=text, expires_at=expires_at)
            return redirect('context_detail', slug=newContext.slug)
        return render(request, 'mytools/context.html', {'form': form})
    form = ContextForm()
    return render(request, 'mytools/context.html', {'form': form})


def context_detail(request, slug):
    contextObject = get_object_or_404(Context, slug=slug)
    if contextObject.expires_at < timezone.now() and not request.user.is_superuser:
        contextObject.is_active = False
        contextObject.save()
        raise PermissionDenied()
    return render(request, 'mytools/context_detail.html', {'context': contextObject})