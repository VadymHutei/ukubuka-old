#!/bin/bash

docker stop uapp
docker rm uapp
docker rmi uapp
docker build -t uapp .
docker run --name uapp -d --restart always -p 80:80 uapp