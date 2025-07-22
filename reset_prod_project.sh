#!/bin/sh

docker compose down
sudo rm -Rf ./staticfiles/*
sudo rm -Rf ./mediafiles/*
docker build -t django:latet . --no-cache
docker-compose --file=docker-compose.yaml up --detach
