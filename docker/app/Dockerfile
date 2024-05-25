FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1  

RUN apt-get update && apt-get -y install \
    tesseract-ocr \
    ffmpeg \
    libsm6 \
    libxext6 \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app 
COPY ./app/requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app 

EXPOSE 8000

CMD ["sh", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]
