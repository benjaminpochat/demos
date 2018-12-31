#!/usr/bin/env bash

# build an image for x86 processor architecture (intel)
docker build . -f ./src/package/Dockerfile-x86 -t x86/delib-archiver:0.0.3

# build an image for arm processor architecture (raspberry)
docker build . -f ./src/package/Dockerfile-arm -t arm/delib-archiver:0.0.3