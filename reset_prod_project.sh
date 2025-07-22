#!/bin/sh

docker compose down
sudo rm -Rf ./staticfiles/*
sudo rm -Rf ./mediafiles/*
docker build --no-cache
docker-compose --file=docker-compose.yaml up --detach
