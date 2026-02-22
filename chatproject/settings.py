import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------
# Security
# -------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# -------------------------------------------------------
# CSRF — Allow ngrok and custom origins
# -------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.app",
    "https://*.ngrok.io",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
# Append any extra trusted origins from environment
_extra_origins = os.getenv("CSRF_TRUSTED_ORIGINS", "")
if _extra_origins:
    CSRF_TRUSTED_ORIGINS += [o.strip() for o in _extra_origins.split(",") if o.strip()]

# Trust X-Forwarded-Proto header (ngrok sends HTTPS)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -------------------------------------------------------
# Installed apps
# -------------------------------------------------------
INSTALLED_APPS = [
    "daphne",        # ASGI server (must be before django apps)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "channels",      # WebSockets
    "chatapp",       # Your chat app
    "rest_framework",
]

# -------------------------------------------------------
# Middleware
# -------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "chatproject.urls"

# -------------------------------------------------------
# Templates
# -------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "chatapp" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "chatproject.wsgi.application"
ASGI_APPLICATION = "chatproject.asgi.application"

# -------------------------------------------------------
# Database (PostgreSQL)
# -------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "chatdb"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "chatpass123"),
        "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# -------------------------------------------------------
# Channel Layer — Redis (with InMemory fallback)
# -------------------------------------------------------
REDIS_URL = os.getenv("REDIS_URL", "")

if REDIS_URL:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [REDIS_URL],
            },
        },
    }
else:
    # Fallback for local development without Docker
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    }

# -------------------------------------------------------
# Static files
# -------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# -------------------------------------------------------
# Authentication
# -------------------------------------------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/login-redirect/"
LOGOUT_REDIRECT_URL = "/login/"

# -------------------------------------------------------
# Uploads
# -------------------------------------------------------
MAX_UPLOAD_SIZE = 1024 * 1024 * 1024  # 1 GB

# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
