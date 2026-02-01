import os
import django

# 1. Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User

# 2. Check if user exists, if not, create it
def create_user():
    username = 'demo'
    password = 'demo12345'
    email = 'demo@example.com'

    if not User.objects.filter(username=username).exists():
        print(f"⚠️ User '{username}' not found. Creating...")
        User.objects.create_superuser(username, email, password)
        print(f"✅ User '{username}' created successfully!")
    else:
        print(f"ℹ️ User '{username}' already exists.")

if __name__ == "__main__":
    create_user()