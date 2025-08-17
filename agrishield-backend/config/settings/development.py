"""
Development settings for AgriShield.
Extends base.py
"""

from .base import *

# ------------------------
# DEBUG & HOSTS
# ------------------------
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ------------------------
# EMAIL BACKEND (use console for dev)
# ------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ------------------------
# DEV LOGGING
# ------------------------
LOGGING["root"]["level"] = "DEBUG"
