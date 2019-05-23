# Use an official Python runtime as a parent image
FROM python:3.5-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
RUN mkdir -p /app/src/main
RUN mkdir -p /app/src/package
COPY ./src/main /app/src/main
COPY ./src/package /app/src/package

# Install gcc
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get -y install gcc

# Install any needed packages specified in requirements-light.txt
RUN mkdir /wheels
RUN pip install -U pip
RUN pip install -U setuptools
RUN pip install wheel
RUN pip wheel --wheel-dir=/wheels -r /app/src/package/docker/scraper/requirements.txt
RUN pip install -f /wheels --no-index -r /app/src/package/docker/scraper/requirements.txt

ENV PYTHONPATH /app:/usr/local/lib/python3.5/site-packages
ENV DEMOS_HOME /app

# Run app.py when the container launches
ENTRYPOINT ["python3", "/app/src/main/python/launcher/main_launcher.py"]
