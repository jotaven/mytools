from django.shortcuts import render, HttpResponse
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
        response = requests.post(f'{API_URL}/qrcode', params={'url': text})
        if response.status_code == 200:
            imagem = base64.b64encode(response.content).decode('utf-8')
            return render(request, 'mytools/qrcode.html', {'imagem': imagem, 'text': text})
        else:
            return render(request, 'mytools/qrcode.html', {'error': 'Falha ao gerar QrCode!'})

    return render(request, 'mytools/qrcode.html')

def ocr(request):
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

def read_qrcode(request):
    if request.method == 'POST':
        if 'file_upload' not in request.FILES:
            print(request.FILES)
            return render(request, 'mytools/read_qrcode.html', {'error': 'Imagem não providenciada!'})
        extension = request.FILES['file_upload'].name.split('.')[-1]
        if extension not in ['jpg', 'jpeg', 'png']:
            return render(request, 'mytools/read_qrcode.html', {'error': f'Formato {extension} não suportado!'})
        

        image = cv2.imdecode(np.fromstring(request.FILES['file_upload'].read(), np.uint8), cv2.IMREAD_COLOR)
        qrcdetector = cv2.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode =  qrcdetector.detectAndDecodeMulti(image)
        if points is not None:
            return render(request, 'mytools/read_qrcode.html', {'qrcode_texts': decoded_info})
        
        return render(request, 'mytools/read_qrcode.html', {'error': 'Nenhum QR Code encontrado!'})

    return render(request, 'mytools/read_qrcode.html')

        
def removebg(request):
    if request.method == "POST" and request.FILES['file_upload']:
        image = request.FILES['file_upload']
        response = requests.get(f'{API_URL}/removebg', files={'image': image})
        if response.status_code == 200:
            imagem = base64.b64encode(response.content).decode('utf-8')
            return render(request, 'mytools/removebg.html', {'imagem': imagem})
        else:
            return render(request, 'mytools/removebg.html', {'error': f'Erro {response.status_code}. Tente novamente mais tarde!'})

    return render(request, 'mytools/removebg.html')

def download_image(request):
    if request.method == "POST" and 'imagem' in request.POST:
        imagem = base64.b64decode(request.POST.get('imagem'))
        response = HttpResponse(imagem, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
        return response

