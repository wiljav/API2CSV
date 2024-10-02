#!/bin/bash

# Define the directory for MinIO data
minio_data_dir="./apps/minio_data"

# Check if the directory exists
if [ -d "$minio_data_dir" ]; then
  echo "Directory $minio_data_dir exists. Cleaning it..."
  # Remove all files in the directory
  rm -rf "$minio_data_dir/*"
else
  echo "Directory $minio_data_dir doesn't exist. Creating it..."
  # Create the directory if it doesn't exist
  mkdir -p "$minio_data_dir"
fi

# Create a Python virtual environment
echo "Creating Python virtual environment..."
python -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages from requirements.txt
echo "Installing requirements from requirements.txt..."
pip install -r requirements.txt

# Running Docker Compose
echo "Running Docker Compose..."
docker-compose --env-file ./docker_compose_keys.env up -d
python3 ./main.py