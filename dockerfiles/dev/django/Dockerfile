FROM python:3.10-slim-buster

LABEL maintainer="mjz589.2018@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./core .
 
 