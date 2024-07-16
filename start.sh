#!/bin/bash

#Should tear down everything just in case(?)
docker-compose down

#Start docker-compose.yml
docker-compose up -d --build