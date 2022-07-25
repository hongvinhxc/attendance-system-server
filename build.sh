#!/bin/bash

# Build docker image
docker build -t attendance-server:latest .

# Compose container
docker-compose up -d attendance-server

echo "";