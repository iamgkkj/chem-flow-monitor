# Create and activate virtual environment
python3 -m venv ../.venv
source ../.venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and setup database
python ../backend/manage.py migrate
python ../backend/manage.py createsuperuser --username demo --email demo@example.com
# (Set password to 'demo12345' to match the guide below, or choose your own)

# Start the server
python ../backend/manage.py runserver

# Run the desktop app
.venv/bin/python main.py