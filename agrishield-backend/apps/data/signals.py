import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.data.models import FloodIndicator
from apps.data.processors.risk_processor import RiskProcessor

logger = logging.getLogger(__name__)

@receiver(post_save, sender=FloodIndicator)
def process_risk_on_new_indicator(sender, instance, created, **kwargs):
    """
    When a new indicator (river level, rainfall, etc.) is saved,
    trigger risk calculation.
    """
    if created:
        try:
            RiskProcessor.calculate_for_village(instance.village)
            logger.info(f"✅ Risk recalculated for village {instance.village.name}")
        except Exception as e:
            logger.error(f"❌ Failed to process risk for {instance.village.name}: {str(e)}")
