# Setup environment
if (!(Test-Path "../.venv")) {
    python -m venv ../.venv
}
& ../.venv/Scripts/Activate.ps1

# Install dependencies
pip install -r ../requirements.txt
pip install -r requirements.txt

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
