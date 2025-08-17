import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Alert

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Alert)
def handle_new_alert(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New alert issued: {instance}")
        # Later: integrate SMS, push notifications, etc.
