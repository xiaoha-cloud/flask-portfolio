#!/bin/bash

set -e

echo "Killing all tmux sessions..."
tmux ls 2>/dev/null | awk -F: '{print $1}' | xargs -r -I {} tmux kill-session -t {}

echo "Going to project directory..."
cd ~/flask-portfolio

echo "Pulling latest code from GitHub..."
git fetch && git reset origin/main --hard

echo "Activating virtual environment..."
source python3-virtualenv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting Flask app in tmux (detached)..."
tmux new-session -d -s flask_server "bash -c 'cd ~/flask-portfolio && source python3-virtualenv/bin/activate && mkdir -p errors && LOGFILE=errors/\$(date +\"%Y-%m-%d_%H-%M-%S\")-flask.log && flask run --host=0.0.0.0 --port=5001 2>&1 | tee \$LOGFILE'"

echo "Site redeployed successfully!"
