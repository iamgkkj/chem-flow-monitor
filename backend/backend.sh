#!/bin/bash

# Setup environment
cd "$(dirname "$0")"
cd ..
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Database setup
python3 backend/manage.py migrate
python3 backend/create_demo_user.py

# Start server
python3 backend/manage.py runserver
