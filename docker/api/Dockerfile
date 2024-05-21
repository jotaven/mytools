FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN apt-get update \
  && apt-get -y install ffmpeg libsm6 libxext6

WORKDIR /api 
COPY ./api/requirements.txt /api


RUN pip3 install -r requirements.txt --no-cache-dir
COPY ./api /api 


EXPOSE 8001

CMD ["python", "main.py"]
