#!/bin/bash

#Should tear down everything just in case(?)
docker-compose down

# Check if the image exists and remove it if it does
if docker images -q "vpn-network_web_vpn:latest" > /dev/null 2>&1; then
  docker rmi vpn-network_web_vpn:latest
fi


#Start docker-compose.yml
docker-compose up -d --build