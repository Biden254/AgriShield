# apps/alerts/apps.py

from django.apps import AppConfig


class AlertsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.alerts"
    verbose_name = "Disaster Alerts"

    def ready(self):
        """
        Import signals or perform startup logic for the alerts app.
        Example: register signal handlers for alert creation/delivery.
        """
        try:
            import apps.alerts.signals  # noqa
        except ImportError:
            pass
