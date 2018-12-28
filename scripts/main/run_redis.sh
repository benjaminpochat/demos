#!/usr/bin/env bash
docker run --name redis-server --restart=always -d -v /data/redis:/data -p 6379:6379 redis:5.0.3 redis-server --dir /data --save 900 1 --save 300 10 --save 60 10000
