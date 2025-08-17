import logging
from apps.data.fetchers.openmeteo_fetcher import OpenMeteoFetcher
from apps.data.fetchers.wra_fetchers import WRAFetcher
from apps.core.models import Village

logger = logging.getLogger(__name__)


class DataServices:
    """
    Coordinates fetching and saving of flood-related data
    from different sources (Open-Meteo, WRA, Indigenous, etc.)
    """

    @staticmethod
    def fetch_openmeteo_data():
        villages = Village.objects.all()
        success_count = 0

        for village in villages:
            if OpenMeteoFetcher.fetch_weather(village):
                success_count += 1

        logger.info(f"✅ OpenMeteo data fetched for {success_count}/{villages.count()} villages.")
        return success_count

    @staticmethod
    def fetch_wra_data():
        success = WRAFetcher.fetch_river_levels()
        if success:
            logger.info("✅ WRA river levels fetched successfully.")
        else:
            logger.warning("⚠️ Failed to fetch WRA data.")
        return success
