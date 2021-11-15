FROM python:3.8.5-alpine

COPY . /app
WORKDIR /app

# RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base


RUN pip install -r requirements.txt

