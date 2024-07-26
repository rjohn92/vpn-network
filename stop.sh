#!/bin/bash

#stop and remove the containers, networks, volumes in the docker-compose
docker-compose down

#remove the images too
docker rmi vpn-network_web-vpn:latest
