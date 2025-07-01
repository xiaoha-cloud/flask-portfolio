#!/bin/bash

# Redeploy Site Script
# This script automates the redeployment process for the Flask portfolio site

echo "Starting redeployment process..."

# Step 1: Kill all existing tmux sessions
echo "Killing existing tmux sessions..."
tmux kill-server 2>/dev/null || true

# Step 2: Navigate to project directory
echo "Navigating to project directory..."
cd ~/flask-portfolio || {
    echo "Error: Could not find flask-portfolio directory"
    exit 1
}

# Step 3: Update git repository with latest changes
echo "Fetching and resetting to latest changes from GitHub..."
git fetch && git reset origin/main --hard || {
    echo "Error: Failed to update git repository"
    exit 1
}

# Step 4: Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source python3-virtualenv/bin/activate || {
    echo "Error: Failed to activate virtual environment"
    exit 1
}

pip install -r requirements.txt || {
    echo "Error: Failed to install Python dependencies"
    exit 1
}

# Step 5: Start new detached tmux session with Flask server
echo "Starting Flask server in new tmux session..."
tmux new-session -d -s flask-server -c ~/flask-portfolio << EOF
source python3-virtualenv/bin/activate
export FLASK_APP=app
export FLASK_ENV=production
python -m flask run --host=0.0.0.0 --port=5000
EOF

# Wait a moment for the server to start
sleep 3

# Check if the tmux session is running
if tmux has-session -t flask-server 2>/dev/null; then
    echo "Redeployment completed successfully!"
    echo "Flask server is running in tmux session 'flask-server'"
    echo "You can check the server status with: tmux attach -t flask-server"
    echo "To detach from the session, press Ctrl+B then D"
else
    echo "Error: Failed to start Flask server"
    exit 1
fi
