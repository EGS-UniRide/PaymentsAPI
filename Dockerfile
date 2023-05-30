# Payments API Docker File
# Rodrigo Martins
# sudo docker build -t paymentsapi .


FROM python:3.10-alpine

MAINTAINER Rodrigo Martins

LABEL version="1.0"

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./src /app/src

COPY paymentsAPI.py /app/paymentsAPI.py
COPY .env /app/.env

EXPOSE 8000/tcp

CMD ["uvicorn", "paymentsAPI:app", "--host", "0.0.0.0", "--port", "8000"]