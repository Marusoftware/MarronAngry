#! /bin/bash

docker buildx build --platform linux/amd64 -t marusoftware/marron:latest -o type=docker,push=false,name=marron-amd64,dest=/home/maruo/marron-amd64.tar -f Dockerfile_production .
docker buildx build --platform linux/arm64/v8 -t marusoftware/marron:latest -o type=docker,push=false,name=marron-arm64,dest=/home/maruo/marron-arm64.tar -f Dockerfile_production .