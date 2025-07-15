#!/bin/bash

LOGFILE="errors/\$(date +\'%Y-%m-%d_%H-%M-%S\')"

echo "Going to project directory..."
cd ~/flask-portfolio

echo "Pulling latest code from GitHub..."
git fetch && git reset origin/main --hard

echo "Activating virtual environment..."
source python3-virtualenv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Restarting myportfolio service..."
sudo systemctl restart myportfolio 2>> $LOGFILE

echo "Site redeployed successfully!"
