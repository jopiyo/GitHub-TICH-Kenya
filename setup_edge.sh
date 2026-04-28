#!/bin/bash

# Install Docker and Git
sudo apt-get update
sudo apt-get install -y docker.io git python3-pip

# Add user to docker group (requires logout to take effect)
sudo usermod -aG docker $USER

# Setup project directories
mkdir -p data/raw data/processed models docs scripts src web

echo "Environment ready. Please log out and back in to finalize Docker permissions."
