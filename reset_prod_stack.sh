#!/bin/bash
#
# Use this script during development when containerized
# when resetting the containerized state to base

# Exit immediately if any command fails
set -e

# Get the file path of this script
root=$(dirname "$(realpath "$0")")
django_root="$root/django"

# Function to print action messages
log_action() {
    echo "==> $1"
}


# Function to ask yes/no question
ask_yes_no() {
    while true; do
        read -p "$1 [y/n]: " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

# Process each item in the root directory
for item in "$django_root"/*; do
    # Delete the sqlite3 database
    if [[ "$(basename "$item")" == "db.sqlite3" ]]; then
        if [[ -f "$item" ]]; then
            rm -f "$item"
            log_action "$item"
        fi
    fi
    
    # Process directories
    if [[ -d "$item" ]]; then
        dir_name=$(basename "$item")
        echo "> $item"
        
        # Delete USER UPLOADED MEDIA folder contents
        if [[ "$dir_name" == "mediafiles" || "$dir_name" == "staticfiles" ]]; then
            for subitem in "$item"/*; do
                if [[ "$dir_name" == "mediafiles" && "$(basename "$subitem")" == "default.jpg" ]]; then
                    continue
                fi
                if [[ -d "$subitem" ]]; then
                    rm -rf "$subitem"
                    log_action "$subitem"
                    elif [[ -f "$subitem" ]]; then
                    rm -f "$subitem"
                    log_action "$subitem"
                fi
            done
        fi
        
        # Process subdirectories
        for subitem in "$item"/*; do
            if [[ -e "$subitem" ]]; then
                subitem_name=$(basename "$subitem")
                echo ">> $subitem"
                
                # Clear out the APP MIGRATIONS files
                if [[ "$subitem_name" == "migrations" && -d "$subitem" ]]; then
                    echo ">>> $subitem"
                    for file in "$subitem"/*; do
                        if [[ "$(basename "$file")" != "__init__.py" && -f "$file" ]]; then
                            rm -f "$file"
                            log_action "$file"
                        fi
                    done
                fi
                
                # Clear out the PYCACHE files
                if [[ "$subitem_name" == "__pycache__" && -d "$subitem" ]]; then
                    echo ">>> $subitem"
                    for file in "$subitem"/*; do
                        if [[ "$(basename "$file")" != "__init__.py" && -f "$file" ]]; then
                            rm -f "$file"
                            log_action "$file"
                        fi
                    done
                fi
            fi
        done
    fi
done

log_action "Stopping containers..."
docker compose down --volumes --rmi all

log_action "Cleaning static files..."
rm -rf "${django_root}/staticfiles/"*

log_action "Cleaning media files (except default.jpg)..."
find "${django_root}/mediafiles/" -mindepth 1 -not -name 'default.jpg' -delete

if ask_yes_no "Do you want to rebuild the images?"; then
    log_action "Rebuilding Docker image(s)..."
    docker build --no-cache -t d-django:latest --file "${django_root}/Dockerfile.django" "${django_root}"
    docker build --no-cache -t d-nginx:latest --file "${root}/nginx/Dockerfile.nginx" "${root}/nginx"
fi

if ask_yes_no "Do you want to rebuild the images?"; then
    log_action "Starting containers in detached mode..."
    docker compose --file="${root}/docker-compose.yaml" up --detach
fi

echo "Reset complete."
