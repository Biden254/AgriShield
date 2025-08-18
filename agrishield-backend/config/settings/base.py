"""
Django base settings for AgriShield project.
Shared across development and production.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# ------------------------
# PATHS
# ------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ------------------------
# SECURITY
# ------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key")  # Override in production
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# ------------------------
# APPLICATIONS
# ------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
]

LOCAL_APPS = [
    "apps.users",
    "apps.alerts",
    "apps.integrations",
    "apps.core",
    "apps.data",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ------------------------
# MIDDLEWARE
# ------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Keep CORS at the top
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# WhiteNoise for static files in production
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------
# URLS & WSGI
# ------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ------------------------
# DATABASE
# ------------------------
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.mysql"),
        "NAME": os.getenv("DB_NAME", "agrishield_db"),
        "USER": os.getenv("DB_USER", "agrishield_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "G0r1ll@p3"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ------------------------
# AUTH & USER MODEL
# ------------------------
AUTH_USER_MODEL = "users.User"  # Custom user model

# ------------------------
# PASSWORD VALIDATORS
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------
# INTERNATIONALIZATION
# ------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

# ------------------------
# STATIC & MEDIA
# ------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # For collectstatic

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------
# TEMPLATES
# ------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ------------------------
# DJANGO REST FRAMEWORK
# ------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # Change to IsAuthenticated in prod
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

# ------------------------
# CORS
# ------------------------
CORS_ALLOWED_ORIGINS = [
    "https://agrishield-one.vercel.app",  # Production frontend
    "http://localhost:3000",             # Local development
]
CORS_ALLOW_ALL_ORIGINS = False  # Keep strict in production

# ------------------------
# AFRICA'S TALKING SMS/USSD
# ------------------------
AT_API_KEY = os.getenv("AT_API_KEY", "")
AT_USERNAME = os.getenv("AT_USERNAME", "")
SMS_PROVIDER = os.getenv("SMS_PROVIDER", "AFRICASTALKING")
SMS_SENDER_ID = os.getenv("SMS_SENDER_ID", "")

# ------------------------
# LOGGING
# ------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
