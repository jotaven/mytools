FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1  

RUN apt-get update && apt-get -y install ffmpeg libsm6 libxext6 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /api 
COPY ./api/requirements.txt /api

RUN pip install --no-cache-dir -r requirements.txt
COPY ./api /api 

EXPOSE 8001

CMD ["python", "main.py"]
