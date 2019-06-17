FROM tensorflow/serving:1.13.0

RUN mkdir -p /models/demos/1/variables
COPY ./src/main/resources/mlp_model.pb /models/demos/1/saved_model.pb
COPY ./src/package/docker/classifier/variables.index /models/demos/1/variables/variables.index
COPY ./src/package/docker/classifier/variables.data-00000-of-00001 /models/demos/1/variables/variables.data-00000-of-00001

