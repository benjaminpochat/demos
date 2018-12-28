# Use an official Python runtime as a parent image
FROM python:3.5

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY .. /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV PYTHONPATH /app:/usr/local/lib/python3.5/site-packages

# Run app.py when the container launches
CMD ["python3", "/app/src/main/python/process/training/training_data_producer/training_data_collector.py"]
