#!/bin/bash

# Redeploy Site Script
# This script automates the redeployment process for the Flask portfolio site using systemd service

echo "Starting redeployment process..."

# Step 1: Navigate to project directory
echo "Navigating to project directory..."
cd ~/flask-portfolio || {
    echo "Error: Could not find flask-portfolio directory"
    exit 1
}

echo "Current git remote:"
git remote -v

# Step 2: Update git repository with latest changes
echo "Fetching and resetting to latest changes from GitHub..."
git fetch && git reset origin/main --hard || {
    echo "Error: Failed to update git repository"
    exit 1
}

# Step 3: Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source python3-virtualenv/bin/activate || {
    echo "Error: Failed to activate virtual environment"
    exit 1
}

pip install -r requirements.txt || {
    echo "Error: Failed to install Python dependencies"
    exit 1
}

# Step 4: Restart myportfolio service
echo "Restarting myportfolio service..."
sudo systemctl restart myportfolio || {
    echo "Error: Failed to restart myportfolio service"
    exit 1
}

# Wait a moment for the service to start
sleep 3

# Check if the service is running
if sudo systemctl is-active --quiet myportfolio; then
    echo "Redeployment completed successfully!"
    echo "Flask server is running as systemd service 'myportfolio'"
    echo "You can check the service status with: sudo systemctl status myportfolio"
    echo "You can view logs with: sudo journalctl -u myportfolio -f"
    echo "Website is accessible at: http://jememaflask.duckdns.org:5000"
else
    echo "Error: Failed to start myportfolio service"
    echo "Check service logs with: sudo journalctl -u myportfolio"
    exit 1
fi
