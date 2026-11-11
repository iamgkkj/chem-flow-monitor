"""Create the demo user used by the web and desktop clients.

Thin wrapper around the `ensure_demo_user` management command so this script
keeps working for the local setup helpers (backend.sh / backend.ps1).

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

from django.core.management import call_command


if __name__ == "__main__":
    if os.environ.get("CREATE_DEMO_USER", "true").lower() in ("false", "0", "no", "off"):
        print("↷️  Skipping demo user creation (CREATE_DEMO_USER is disabled).")
    else:
        call_command("ensure_demo_user")
