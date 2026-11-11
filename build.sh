#!/usr/bin/env bash
# Build script executed by Render on every deploy of the Django backend.
# Exit immediately if a command fails.
set -o errexit

echo "==> Installing Python dependencies"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "==> Collecting static files"
python backend/manage.py collectstatic --noinput --clear

echo "==> Applying database migrations"
python backend/manage.py migrate --noinput

echo "==> Seeding the demo user"
python backend/create_demo_user.py

echo "==> Build finished"
