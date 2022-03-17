FROM python:3.9.6
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD backend_youtube_dl.py /usr/local/lib/python3.9/site-packages/pafy
ADD ffmpeg.exe /usr/local/lib
COPY . /app