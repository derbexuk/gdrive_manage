FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /code

ADD requirements.txt .
RUN  pip3 install -r requirements.txt

COPY ./*.py ./
COPY ./creds.json ./
