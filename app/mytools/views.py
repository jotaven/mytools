from django.shortcuts import render
import base64
import requests
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

TESSDATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data/tessdata')

def index(request):
    return render(request, 'mytools/index.html')

def qrcode(request):
    if request.method == 'POST':
        if 'url' not in request.POST:
            return render(request, 'mytools/qrcode.html', {'error': 'URL not provided!'})
        url = request.POST.get('url')
        response = requests.get('http://127.0.0.1:8001/qrcode', params={'url': url})
        if response.status_code == 200:
            imagem = base64.b64encode(response.content).decode('utf-8')
            return render(request, 'mytools/qrcode.html', {'imagem': imagem, 'url': url})
        else:
            return render(request, 'mytools/qrcode.html', {'error': 'Failed to generate QR code!'})

    return render(request, 'mytools/qrcode.html')

def ocr(request):
    print(request.FILES)
    if request.method == 'POST':
        if 'file_upload' not in request.FILES:
            return render(request, 'mytools/ocr.html', {'error': 'Image not provided!'})
        image = Image.open(request.FILES['file_upload'])
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        resultado = pytesseract.image_to_data(image, lang="por", config=f"--tessdata-dir '{TESSDATA_DIR}'", output_type=pytesseract.Output.DICT)
        resultado = [resultado['text'][i] for i in range(len(resultado['text'])) if resultado['text'][i] != '' and resultado['conf'][i] > 45]
        resultado = ' '.join(resultado)
        return render(request, 'mytools/ocr.html', {'image_text': resultado})

    return render(request, 'mytools/ocr.html')