"""
Production settings for AgriShield.
Extends base.py
"""

from .base import *

# ------------------------
# SECURITY
# ------------------------
DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "agrishield.com").split(",")

# Secure settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ------------------------
# EMAIL (example with SMTP)
# ------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

# ------------------------
# PROD LOGGING
# ------------------------
LOGGING["root"]["level"] = "WARNING"
