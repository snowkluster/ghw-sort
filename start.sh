#!/bin/sh

Green="\e[32m"
Red="\033[0;31m"
Blue='\033[0;34m'
NC='\033[0m'

if [ "$1" = "stop" ]; then
    echo "${Red}Stopping containers and removing created image${NC}"
    sudo docker stop ghw-flask-app
    sudo docker rm ghw-flask-app
    sudo docker rmi flask-app
    exit 0
fi

sudo docker build -t flask-app .
sudo docker run -p 5000:5000 --name ghw-flask-app flask-app