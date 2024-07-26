#!/bin/bash

#Should tear down everything just in case(?)
docker-compose down

if [ docker images -q "$1" > /dev/null 2>&1 vpn-network_web_vpn:latest ]; then
  docker rmi vpn-network_web_vpn:latest	
fi


#Start docker-compose.yml
docker-compose up -d --build