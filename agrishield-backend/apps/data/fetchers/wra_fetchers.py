import requests
import logging
from django.conf import settings
from django.utils import timezone
from apps.data.models import FloodIndicator, Village

logger = logging.getLogger(__name__)

class WRAFetcher:
    API_URL = "https://api.wra.go.ke/river-levels"
    
    @classmethod
    def fetch_river_levels(cls):
        try:
            headers = {'Authorization': f'Bearer {settings.WRA_API_KEY}'}
            response = requests.get(cls.API_URL, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            river_data = data.get('nzoia', {})
            
            # Save to database
            for village_name, level in river_data.items():
                village = Village.objects.get(name=village_name)
                FloodIndicator.objects.create(
                    indicator_type='RIVER_LEVEL',
                    value=level,
                    village=village,
                    confidence=0.9  # High confidence for official data
                )
            
            return True
        except Exception as e:
            logger.error(f"Failed to fetch WRA data: {str(e)}")
            return False