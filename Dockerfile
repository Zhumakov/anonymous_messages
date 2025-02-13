FROM python:3.12

WORKDIR source/

COPY requirements.txt

RUN pip install -r requirements.txt

COPY . .
