FROM ubuntu
# RUN apt update \
# && apt-get install -y vlc

FROM library/postgres
ENV POSTGRES_USER test
ENV POSTGRES_PASSWORD test
ENV POSTGRES_DB player

FROM python:3.10.2
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY vlc-3.0.16.tar.xz /app/vlc-3.0.16.tar.xz
RUN pip install -r requirements.txt
COPY . /app

# use docker-compose to run the app