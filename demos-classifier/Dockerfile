FROM python:3.7.0-slim

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get -y install gcc

RUN pip install -U pip
RUN pip install -U setuptools

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

RUN useradd --create-home demos
WORKDIR /home/demos
USER demos

ENV PYTHONPATH .:/usr/local/lib/python3.7/site-packages
ENV DEMOS_HOME .

RUN mkdir -p ./src/main
COPY ./src/main ./src/main

ENTRYPOINT ["python3", "./src/main/python/main.py"]