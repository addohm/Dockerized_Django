#!/bin/sh
# Use this script during development when containerized
# when resetting the containerized state to base

docker compose down
sudo rm -Rf ./staticfiles/*
sudo rm -Rf ./mediafiles/*
docker build -t django:latest . --no-cache
docker-compose --file=docker-compose.yaml up --detach
