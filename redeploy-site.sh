#!/bin/bash

set -e

echo "Starting redeployment process"

# Change to project directory, exit if not found
cd /root/flask-portfolio || {
    echo "Error: Could not find /root/flask-portfolio directory"
    exit 1
}

# Pull latest changes from main branch
echo "Updating code from Git"
git fetch && git reset --hard origin/main || {
    echo "Error: Failed to update git repository"
    exit 1
}

# Stop containers to prevent out of memory issues during build
echo "Stopping Docker containers"
docker compose -f docker-compose.prod.yml down || {
    echo "Error: Failed to stop Docker containers"
    exit 1
}

# Build and start containers
echo "Building and starting Docker containers"
docker compose -f docker-compose.prod.yml up -d --build || {
    echo "Error: Failed to start Docker containers"
    exit 1
}

# Check status
echo "Checking container status"
docker compose -f docker-compose.prod.yml ps

echo "Redeployment completed successfully!"
