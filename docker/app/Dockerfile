FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN apt-get update \
  && apt-get -y install tesseract-ocr \ 
  && apt-get -y install ffmpeg libsm6 libxext6

WORKDIR /app 
COPY ./app/requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY ./app /app 

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
