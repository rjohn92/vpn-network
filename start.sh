#!/bin/bash

#Should tear down everything just in case(?)
docker-compose down

if [ docker images -q "$1" > /dev/null 2>&1 vpn-network_web:latest ]; then
  docker rmi vpn-network_web:latest
fi

if [ docker images -q "$1" > /dev/null 2>&1 vpn-network_vpn:latest ]; then
  docker rmi vpn-network_vpn:latest
fi

#Start docker-compose.yml
docker-compose up -d --build