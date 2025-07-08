#!/bin/bash
cd ~/flask-portfolio
source python3-virtualenv/bin/activate
export FLASK_APP=app
export FLASK_ENV=production
python -m flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 