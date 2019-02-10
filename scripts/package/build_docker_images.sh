#!/usr/bin/env bash

# build an image for x86 processor architecture (intel)
docker build . -f ./src/package/Dockerfile-x86 -t x86/demos:0.0.1

# build an image for arm processor architecture (raspberry)
docker build . -f ./src/package/Dockerfile-arm -t arm/demos:0.0.1