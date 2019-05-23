# Use an official Python runtime as a parent image
FROM tensorflow/serving


# Copy the current directory contents into the container at /app
RUN mkdir -p /models/demos/1/variables
COPY ./src/main/resources/mlp_model.pb /models/demos/1/saved_model.pb
COPY ./src/package/docker/classifier/variables.index /models/demos/1/variables/variables.index
COPY ./src/package/docker/classifier/variables.data-00000-of-00001 /models/demos/1/variables/variables.data-00000-of-00001

