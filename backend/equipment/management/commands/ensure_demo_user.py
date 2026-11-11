"""Management command that creates (or repairs) the demo account.

The web and desktop clients log in with the demo credentials published in
the README, so the account has to exist in whatever database the service is
actually talking to. Running this on every start makes the account
self-healing: it is created when missing and its password is re-synced when
it no longer matches the configured value.

    python manage.py ensure_demo_user
"""

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("true", "1", "yes", "on")


class Command(BaseCommand):
    help = "Create or repair the demo account used by the web/desktop clients."

    def add_arguments(self, parser):
        parser.add_argument("--username", default=os.environ.get("DEMO_USERNAME", "demo"))
        parser.add_argument("--password", default=os.environ.get("DEMO_PASSWORD", "demo12345"))
        parser.add_argument("--email", default=os.environ.get("DEMO_EMAIL", "demo@example.com"))
        parser.add_argument(
            "--noinput",
            action="store_true",
            help="Accepted for compatibility with other management commands.",
        )

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        email = options["email"]
        sync_password = _env_bool("DEMO_USER_SYNC_PASSWORD", True)

        try:
            user = User.objects.filter(username=username).first()

            if user is None:
                user = User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS(f"✅ Created demo user '{username}'."))
                return

            changed = False
            if not user.is_active or not user.is_staff or not user.is_superuser:
                user.is_active = True
                user.is_staff = True
                user.is_superuser = True
                changed = True

            if sync_password and not user.check_password(password):
                user.set_password(password)
                changed = True

            if changed:
                user.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Repaired demo user '{username}'."))
            else:
                self.stdout.write(f"ℹ️  Demo user '{username}' already exists and is up to date.")
        except Exception as exc:  # never block the service from booting
            self.stderr.write(self.style.WARNING(f"⚠️  Could not prepare demo user '{username}': {exc}"))
