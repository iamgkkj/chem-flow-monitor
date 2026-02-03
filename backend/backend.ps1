# Setup environment
# Navigate to project root (one level up from backend/)
Set-Location "$PSScriptRoot/.."

if (!(Test-Path ".venv")) {
    python -m venv .venv
}
& .venv/Scripts/Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
pip install Django djangorestframework django-cors-headers gunicorn pandas reportlab --only-binary :all:

# Database setup
python backend/manage.py migrate
python backend/create_demo_user.py

# Start server
python backend/manage.py runserver
