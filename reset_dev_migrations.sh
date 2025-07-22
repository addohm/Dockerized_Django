#!/bin/bash

# Get the file path of this script
root=$(dirname "$(realpath "$0")")

# Function to print deletion messages
delete_msg() {
  echo "- $1"
}

# Process each item in the root directory
for item in "$root"/*; do
  # Delete the sqlite3 database
  if [[ "$(basename "$item")" == "db.sqlite3" ]]; then
    if [[ -f "$item" ]]; then
      rm -f "$item"
      delete_msg "$item"
    fi
  fi

  # Process directories
  if [[ -d "$item" ]]; then
    dir_name=$(basename "$item")
    echo "> $item"

    # Delete USER UPLOADED MEDIA folder contents
    if [[ "$dir_name" == "mediafiles" || "$dir_name" == "staticfiles" ]]; then
      for subitem in "$item"/*; do
        if [[ -d "$subitem" ]]; then
          rm -rf "$subitem"
          delete_msg "$subitem"
        elif [[ -f "$subitem" ]]; then
          rm -f "$subitem"
          delete_msg "$subitem"
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
              delete_msg "$file"
            fi
          done
        fi

        # Clear out the PYCACHE files
        if [[ "$subitem_name" == "__pycache__" && -d "$subitem" ]]; then
          echo ">>> $subitem"
          for file in "$subitem"/*; do
            if [[ "$(basename "$file")" != "__init__.py" && -f "$file" ]]; then
              rm -f "$file"
              delete_msg "$file"
            fi
          done
        fi
      fi
    done
  fi
done
