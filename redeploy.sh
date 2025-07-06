#!/bin/bash

set -e

echo "Starting redeployment process..."

tmux kill-server 2>/dev/null || true

cd /root/flask-portfolio || {
    echo "Error: Could not find /root/flask-portfolio directory"
    exit 1
}

git fetch && git reset origin/main --hard || {
    echo "Error: Failed to update git repository"
    exit 1
}

source /root/flask-portfolio/python3-virtualenv/bin/activate || {
    echo "Error: Failed to activate virtual environment"
    exit 1
}

pip install -r requirements.txt || {
    echo "Error: Failed to install Python dependencies"
    exit 1
}

tmux new-session -d -s flask-server -c /root/flask-portfolio << EOF
source python3-virtualenv/bin/activate
export URL=localhost:5000
export FLASK_ENV=development
export FLASK_APP=app
python -m flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1
EOF


sleep 3
if tmux has-session -t flask-server 2>/dev/null; then
    echo "Redeployment completed successfully!"
else
    echo "Error: Failed to start Flask server"
    exit 1
fi

