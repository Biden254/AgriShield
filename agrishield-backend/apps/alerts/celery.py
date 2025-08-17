# apps/alerts/tasks.py
from celery import shared_task
from django.utils import timezone
from apps.alerts.models import Alert
from apps.integrations.sms.providers import send_sms

@shared_task
def check_and_trigger_alerts():
    """
    Periodic task:
    - Checks all alerts in the system
    - Triggers notifications if conditions are met
    """
    now = timezone.now()
    alerts = Alert.objects.filter(
        trigger_time__lte=now,
        status="pending"
    )

    for alert in alerts:
        try:
            # Send SMS notification
            message = f"⚠️ Flood Alert for {alert.village.name}: {alert.message}"
            send_sms(alert.farmer.phone_number, message)

            # Mark alert as sent
            alert.status = "sent"
            alert.sent_at = now
            alert.save(update_fields=["status", "sent_at"])

        except Exception as e:
            # In case of failure, mark as failed for retry
            alert.status = "failed"
            alert.error_message = str(e)
            alert.save(update_fields=["status", "error_message"])


@shared_task
def retry_failed_deliveries():
    """
    Periodic task:
    - Retries alerts that previously failed
    """
    failed_alerts = Alert.objects.filter(status="failed")

    for alert in failed_alerts:
        try:
            message = f"⚠️ Flood Alert for {alert.village.name}: {alert.message}"
            send_sms(alert.farmer.phone_number, message)

            # Mark alert as sent
            alert.status = "sent"
            alert.sent_at = timezone.now()
            alert.error_message = None
            alert.save(update_fields=["status", "sent_at", "error_message"])

        except Exception as e:
            # Keep status as failed but update error message
            alert.error_message = str(e)
            alert.save(update_fields=["error_message"])
