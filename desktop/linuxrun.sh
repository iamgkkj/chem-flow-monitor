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
pip install -r desktop/requirements.txt

# Database setup
python3 backend/manage.py migrate
python3 backend/create_demo_user.py

# Start backend in background
python3 backend/manage.py runserver > /dev/null 2>&1 &
BACKEND_PID=$!

# Launch desktop app
cd desktop
python3 main.py

# Cleanup
kill $BACKEND_PID