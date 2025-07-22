#!/bin/bash
#
# Use this script during development when containerized
# when resetting the containerized state to base

# Exit immediately if any command fails
set -e

# Get the file path of this script
root=$(dirname "$(realpath "$0")")

# Function to print action messages
log_action() {
  echo "==> $1"
}

log_action "Stopping containers..."
docker compose down

log_action "Cleaning static files..."
sudo rm -rf "${root}/staticfiles/"*

log_action "Cleaning media files..."
sudo rm -rf "${root}/mediafiles/"*

log_action "Rebuilding Docker image..."
docker build -t django:latest "${root}" --no-cache

log_action "Starting containers in detached mode..."
docker-compose --file="${root}/docker-compose.yaml" up --detach

echo "Reset complete."
