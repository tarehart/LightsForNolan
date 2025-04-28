#!/bin/bash

# Sync the local folder to the Pi, excluding .venv
rsync -avz --delete --exclude='.venv' --exclude='.git' --exclude='__pycache__' ./ tarehart@192.168.0.107:/home/tarehart/LightsForNolan/

# SSH into Pi and run the main script
ssh -t tarehart@192.168.0.107 "cd /home/tarehart/LightsForNolan && ./run.sh"
