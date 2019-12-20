FROM python:3.6

RUN apt-get update && apt-get install -y swig

WORKDIR /nabto-client

COPY . .
