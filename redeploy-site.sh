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

# Activate virtual environment
echo "Activating virtual environment"
source /root/flask-portfolio/python3-virtualenv/bin/activate || {
    echo "Error: Failed to activate virtual environment"
    exit 1
}

# Install dependencies
echo "Installing Python dependencies"
pip install -r requirements.txt || {
    echo "Error: Failed to install dependencies"
    exit 1
}

# Restart the systemd service
echo "Restarting myportfolio service"
sudo systemctl restart myportfolio || {
    echo "Error: Failed to restart myportfolio service"
    exit 1
}

# Check status
echo "Checking service status"
sudo systemctl status myportfolio --no-pager

echo "Redeployment completed successfully!"
