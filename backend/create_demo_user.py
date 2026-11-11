"""Create the demo user used by the web and desktop clients.

Credentials can be overridden with environment variables:

    DEMO_USERNAME  (default: demo)
    DEMO_PASSWORD  (default: demo12345)
    DEMO_EMAIL     (default: demo@example.com)

Set CREATE_DEMO_USER=false to skip creating the account entirely.
"""

import os

import django

# 1. Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User

# 2. Check if user exists, if not, create it
def create_user():
    username = os.environ.get("DEMO_USERNAME", "demo")
    password = os.environ.get("DEMO_PASSWORD", "demo12345")
    email = os.environ.get("DEMO_EMAIL", "demo@example.com")

    if not User.objects.filter(username=username).exists():
        print(f"⚠️  User '{username}' not found. Creating...")
        User.objects.create_superuser(username, email, password)
        print(f"✅ User '{username}' created successfully!")
    else:
        print(f"ℹ️  User '{username}' already exists.")


if __name__ == "__main__":
    if os.environ.get("CREATE_DEMO_USER", "true").lower() in ("false", "0", "no", "off"):
        print("↷️  Skipping demo user creation (CREATE_DEMO_USER is disabled).")
    else:
        create_user()
