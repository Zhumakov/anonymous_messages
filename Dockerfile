FROM python:3.12 slim-buster

WORKDIR source/

COPY ./requirements.txt

RUN pip install -r requirements.txt

COPY . .
