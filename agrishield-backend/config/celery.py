from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Default to production if no environment is set
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.production")
)

app = Celery("agrishield")

# Load settings with CELERY_ prefix from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks across all installed apps
app.autodiscover_tasks()

# Periodic tasks (Celery Beat)
app.conf.beat_schedule = {
    "check-flood-risks-every-6-hours": {
        "task": "apps.alerts.tasks.check_and_trigger_alerts",
        "schedule": 6 * 60 * 60,  # 6 hours
    },
    "resend-failed-alerts-every-hour": {
        "task": "apps.alerts.tasks.retry_failed_deliveries",
        "schedule": 60 * 60,  # 1 hour
    },
}

# Recommended: set timezone explicitly (falls back to Django TIME_ZONE if defined)
app.conf.timezone = os.getenv("TIME_ZONE", "UTC")


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing celery workers."""
    print(f"Request: {self.request!r}")
