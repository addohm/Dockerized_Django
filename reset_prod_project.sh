#!/bin/sh

docker compose down
sudo rm -Rf ./staticfiles/*
sudo rm -Rf ./media/*
sudo rm -Rf ./fileshare/*
docker build -t django:latest .
docker compose up --detach