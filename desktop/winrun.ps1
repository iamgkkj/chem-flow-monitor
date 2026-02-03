# Setup environment
if (!(Test-Path "../.venv")) {
    python -m venv ../.venv
}
& ../.venv/Scripts/Activate.ps1

# Install dependencies
# Install dependencies
python -m pip install --upgrade pip
pip install Django djangorestframework django-cors-headers gunicorn pandas reportlab --only-binary :all:
pip install PyQt5 matplotlib requests --only-binary :all:

# Database setup
python ../backend/manage.py migrate
python ../backend/create_demo_user.py

# Start backend
$BackendProcess = Start-Process python -ArgumentList "../backend/manage.py runserver" -NoNewWindow -PassThru
Start-Sleep -Seconds 2

# Launch desktop app
python main.py

# Cleanup
Stop-Process -Id $BackendProcess.Id -Force
