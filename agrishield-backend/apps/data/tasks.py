import logging
from celery import shared_task
from apps.data.services import DataServices

logger = logging.getLogger(__name__)


@shared_task
def fetch_openmeteo_task():
    """
    Celery task to fetch weather data from OpenMeteo
    """
    try:
        count = DataServices.fetch_openmeteo_data()
        logger.info(f"OpenMeteo task completed: {count} villages updated.")
        return count
    except Exception as e:
        logger.error(f"OpenMeteo task failed: {str(e)}")
        return 0


@shared_task
def fetch_wra_task():
    """
    Celery task to fetch river level data from WRA
    """
    try:
        success = DataServices.fetch_wra_data()
        logger.info(f"WRA task completed: {success}")
        return success
    except Exception as e:
        logger.error(f"WRA task failed: {str(e)}")
        return False
