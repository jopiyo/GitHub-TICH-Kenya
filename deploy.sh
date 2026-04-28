#!/bin/bash

# Configuration
APP_NAME="climateguard-backend"
IMAGE_NAME="climateguard-v1"

echo "--- Starting Deployment for ClimateGuard ---"

# 1. Pull the latest code from the repository
echo "Syncing repository..."
git pull origin main

# 2. Rebuild the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME -f scripts/Dockerfile .

# 3. Stop and remove the old container if it exists
echo "Stopping old container..."
docker stop $APP_NAME || true
docker rm $APP_NAME || true

# 4. Run the new container
# Links the host's 8000 port to the container's 8000
echo "Launching new container..."
docker run -d \
  --name $APP_NAME \
  -p 8000:8000 \
  --restart unless-stopped \
  $IMAGE_NAME

echo "--- Deployment Successful: API is live at http://localhost:8000 ---"
