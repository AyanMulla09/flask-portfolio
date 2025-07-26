#!/bin/bash

set -e

echo "Starting Docker redeployment process"

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

# Stop existing containers to prevent memory issues during rebuild
echo "Stopping existing containers"
docker compose -f docker-compose.prod.yml down || {
    echo "Warning: No existing containers to stop, continuing..."
}

# Build and start containers in detached mode
echo "Building and starting containers"
docker compose -f docker-compose.prod.yml up -d --build || {
    echo "Error: Failed to build and start containers"
    exit 1
}

# Check container status
echo "Checking container status"
docker compose -f docker-compose.prod.yml ps

echo "Docker redeployment completed successfully!"
echo "Your application should be running at http://localhost:5000"
