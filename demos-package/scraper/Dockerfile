FROM python:3.5-slim

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get -y install gcc

RUN mkdir /wheels
RUN pip install -U pip
RUN pip install -U setuptools
RUN pip install wheel

COPY ./demos-package/scraper/requirements.txt ./requirements.txt
RUN pip wheel --wheel-dir=/wheels -r ./requirements.txt
RUN pip install -f /wheels --no-index -r ./requirements.txt

RUN useradd --create-home demos
WORKDIR /home/demos
USER demos

ENV PYTHONPATH .:/usr/local/lib/python3.5/site-packages
ENV DEMOS_HOME .

RUN mkdir -p ./src/main
COPY ./demos-scraper/src/main ./src/main

ENTRYPOINT ["python3", "./src/main/python/launcher/main_launcher.py"]
