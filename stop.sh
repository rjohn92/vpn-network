#!/bin/bash

#stop and remove the containers, networks, volumes in the docker-compose
docker-compose down

#remove our private network that uses the vpn
docker network rm private_network

#remove the images too
docker rmi vpn-network_web_vpn:latest
