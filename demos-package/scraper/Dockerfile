FROM python:3.5-slim

WORKDIR /app

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get -y install gcc

RUN mkdir /wheels
RUN pip install -U pip
RUN pip install -U setuptools
RUN pip install wheel
RUN pip wheel --wheel-dir=/wheels -r /app/src/package/docker/scraper/requirements.txt
RUN pip install -f /wheels --no-index -r /app/src/package/docker/scraper/requirements.txt

ENV PYTHONPATH /app:/usr/local/lib/python3.5/site-packages
ENV DEMOS_HOME /app

RUN mkdir -p /app/src/main
RUN mkdir -p /app/src/package
COPY ./src/main /app/src/main
COPY ./src/package /app/src/package

ENTRYPOINT ["python3", "/app/src/main/python/launcher/main_launcher.py"]
