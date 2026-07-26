#!/bin/bash

# Sync the local folder to the Pi, excluding .venv
rsync -avz --delete --exclude='.venv' --exclude='.git' --exclude='__pycache__' ./ tarehart@10.0.0.119:/home/tarehart/LightsForNolan/

# List the running main.py scripts, for debug purposes
ssh tarehart@192.168.0.107 'ps aux | grep ".venv/bin/python -m main"'

# Kill any currently running main.py scripts
ssh tarehart@192.168.0.107 'ps aux | grep "python -m main" | awk "{print \$2}" | xargs -r kill -9'

# SSH into Pi and run the main script
ssh -t tarehart@10.0.0.119 "cd /home/tarehart/LightsForNolan && ./run.sh"
