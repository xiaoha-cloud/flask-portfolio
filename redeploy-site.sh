#!/bin/bash

set -e

echo "Starting redeployment process..."

# Kill any existing tmux server (ignore errors)
tmux kill-server 2>/dev/null || true

# Change to project directory, exit if not found
cd /root/flask-portfolio || {
    echo "Error: Could not find /root/flask-portfolio directory"
    exit 1
}

# Update git repo to latest main branch, exit if fails
git fetch && git reset --hard origin/main || {
    echo "Error: Failed to update git repository"
    exit 1
}

# Activate virtual environment, exit if fails
source /root/flask-portfolio/python3-virtualenv/bin/activate || {
    echo "Error: Failed to activate virtual environment"
    exit 1
}

# Install dependencies
pip install -r requirements.txt || {
    echo "Error: Failed to install Python dependencies"
    exit 1
}

# Start tmux session running Flask app
tmux new-session -d -s flask-server -c /root/flask-portfolio bash -c '
source /root/flask-portfolio/python3-virtualenv/bin/activate &&
export URL=localhost:5000 &&
export FLASK_ENV=development &&
export FLASK_APP=app &&
python -m flask run --host=0.0.0.0 --port=5000
'

sleep 3

# Check if tmux session is running
if tmux has-session -t flask-server 2>/dev/null; then
    echo "Redeployment completed successfully!"
else
    echo "Error: Failed to start Flask server"
    exit 1
fi

