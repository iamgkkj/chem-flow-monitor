"""
Django settings for config project.

Environment driven so the same codebase runs locally and on Render.

Key environment variables (see README "Deploy to Render"):
    SECRET_KEY           - required in production, generate one on Render
    DEBUG                - "true"/"false" (False on Render, True locally)
    DATABASE_URL         - Postgres connection string (falls back to local SQLite)
    ALLOWED_HOSTS        - comma separated host list
    CORS_ALLOWED_ORIGINS - comma separated list of allowed browser origins
    MEDIA_ROOT           - optional path for uploaded CSVs (persistent disk)
    DEMO_USERNAME / DEMO_PASSWORD / DEMO_EMAIL - seeded demo account
"""

import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def _env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean flag from the environment."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("true", "1", "yes", "on")


def _env_list(name: str, default=None) -> list:
    """Read a comma separated list from the environment."""
    raw = os.environ.get(name)
    items = raw.split(",") if raw else list(default or [])
    return [item.strip() for item in items if item and item.strip()]


# --------------------------------------------------------------------------
# Core security settings
# --------------------------------------------------------------------------

IS_RENDER = "RENDER" in os.environ

# On Render this stays False unless explicitly overridden; locally it is True
# so that the dev server behaves like the dev server.
DEBUG = _env_bool("DEBUG", default=not IS_RENDER)

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    if IS_RENDER:
        raise RuntimeError(
            "SECRET_KEY environment variable is required on Render. "
            "Add it under Environment with the 'Generate' button."
        )
    SECRET_KEY = "django-insecure-local-dev-key-change-me"

# Hosts allowed to serve requests. `.onrender.com` covers every Render
# subdomain; RENDER_EXTERNAL_HOSTNAME is the exact public hostname of the
# service (set automatically by Render).
ALLOWED_HOSTS = _env_list(
    "ALLOWED_HOSTS",
    default=[
        "localhost",
        "127.0.0.1",
        ".onrender.com",
        os.environ.get("RENDER_EXTERNAL_HOSTNAME", ""),
    ],
)

# Render terminates TLS and forwards the original scheme in this header.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# The REST API uses token auth (no cookies); the Django admin uses session
# cookies, so make those secure-only once we are not in DEBUG.
SESSION_COOKIE_SECURE = _env_bool("SESSION_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_SECURE = _env_bool("CSRF_COOKIE_SECURE", default=not DEBUG)

# Render's edge already upgrades http -> https, so the redirect stays opt-in
# (a redirect would also turn the health check into a 301).
SECURE_SSL_REDIRECT = _env_bool("SECURE_SSL_REDIRECT", default=False)

# HTTP Strict Transport Security - opt in with e.g. SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = _env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False)
SECURE_HSTS_PRELOAD = _env_bool("SECURE_HSTS_PRELOAD", default=False)

# --------------------------------------------------------------------------
# Application definition
# --------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'equipment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=int(os.environ.get("DATABASE_CONN_MAX_AGE", "60")),
            conn_health_checks=True,
        ),
    }
else:
    # Local development fallback: SQLite next to manage.py.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# --------------------------------------------------------------------------
# Password validation
# --------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# --------------------------------------------------------------------------
# Internationalization
# --------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# --------------------------------------------------------------------------
# CORS
# --------------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = _env_list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://chem-flow-monitor.onrender.com",
    ],
)

# Allow any *.onrender.com frontend (covers renamed/recreated services).
CORS_ALLOWED_ORIGIN_REGEXES = _env_list(
    "CORS_ALLOWED_ORIGIN_REGEXES",
    default=[r"^https://[a-z0-9-]+\.onrender\.com$"],
)

CORS_ALLOW_CREDENTIALS = True

# --------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# --------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Uploaded CSVs. Mount a Render persistent disk at MEDIA_ROOT (or point this
# at any writable path) if the files must survive redeploys.
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT", BASE_DIR / "media"))

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
