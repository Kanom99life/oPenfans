#!/bin/sh
app="docker.test"
docker build -t ${app} .
docker run -t -p 56733:8000 -d \
  --name=${app} \
  -v $PWD:/app ${app}
