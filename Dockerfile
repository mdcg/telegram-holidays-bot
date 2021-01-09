FROM python:3.9.0-alpine3.10

MAINTAINER MDCG

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/