import logging
import os
from pathlib import Path

import openmeteo_requests
import pandas as pd
import requests_cache
from django.conf import settings
from django.utils import timezone
from retry_requests import retry

from apps.core.models import Village
from apps.data.models import FloodIndicator

logger = logging.getLogger(__name__)

class OpenMeteoFetcher:
    """
    Fetches weather forecast data from Open-Meteo API for a given village,
    saves rainfall data as FloodIndicator objects, and optionally
"""
    API_URL = "https://api.open-meteo.com/v1/forecast"
    HOURLY_VARS = [
        "temperature_2m", "rain", "soil_moisture_3_to_9cm",        
        "wind_speed_80m", "wind_direction_80m", "showers"
    ]
    DAILY_VARS = ["temperature_2m_max", "temperature_2m_min"]
    CURRENT_VARS = ["temperature_2m", "rain", "relative_humidity_2m"]

    def __init__(self, village: Village):
        if not all([village.latitude, village.longitude]):
            raise ValueError(f"Village '{village.name}' is missing latitude or longitude.")
        self.village = village
        self.client = self._setup_client()

    def _setup_client(self):
        """Sets up the Open-Meteo API client with cache and retry."""
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        return openmeteo_requests.Client(session=retry_session)

    def fetch_and_save(self, save_csv=False):
        """
        Fetches weather data, saves rainfall to the database, and optionally
        saves the full forecast to a CSV file.
        """
        params = {
            "latitude": self.village.latitude,
            "longitude": self.village.longitude,
            "hourly": self.HOURLY_VARS,
            "daily": self.DAILY_VARS,
            "current": self.CURRENT_VARS,
            "timezone": "GMT",
            "past_days": 7,
        }
        try:
            responses = self.client.weather_api(self.API_URL, params=params)
            response = responses[0]
            logger.info(f"Successfully fetched weather data for {self.village.name}")
        except Exception as e:
            logger.error(f"Failed to fetch Open-Meteo data for {self.village.name}: {e}")
            return

        hourly_dataframe = self._process_hourly_data(response)
        self._save_rainfall_to_db(hourly_dataframe)

        if save_csv:
            self._save_dataframe_to_csv(hourly_dataframe)

    def _process_hourly_data(self, response):
        """Processes the hourly data part of the API response into a DataFrame."""
        hourly = response.Hourly()
        hourly_data = {"date": pd.to_datetime(hourly.Time(), unit="s", utc=True)}
        
        for i, var_name in enumerate(self.HOURLY_VARS):
            hourly_data[var_name] = hourly.Variables(i).ValuesAsNumpy()

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        return hourly_dataframe

    def _save_rainfall_to_db(self, dataframe: pd.DataFrame):
        """
        Parses the dataframe and saves rainfall data as FloodIndicator objects.
        """
        # Filter for future rainfall predictions
        future_rain = dataframe[dataframe['date'] > timezone.now()]
        
        indicators_to_create = []
        for _, row in future_rain.iterrows():
            if row['rain'] > 0:  # Only save if there's predicted rain
                indicators_to_create.append(
                    FloodIndicator(
                        indicator_type='RAINFALL_FORECAST',
                        value=row['rain'],
                        village=self.village,
                        confidence=0.75,  # Confidence for forecast data
                        timestamp=row['date']
                    )
                )
        
        if indicators_to_create:
            FloodIndicator.objects.bulk_create(indicators_to_create, ignore_conflicts=True)
            logger.info(f"Saved {len(indicators_to_create)} rainfall forecasts for {self.village.name}")

    def _save_dataframe_to_csv(self, dataframe: pd.DataFrame):
        """Saves the full hourly data to a CSV in a consistent location."""
        # Create a 'data_exports' directory in the project root if it doesn't exist
        output_dir = Path(settings.BASE_DIR) / 'data_exports'
        os.makedirs(output_dir, exist_ok=True)

        # Consistent filename based on village and date
        today = timezone.now().strftime('%Y-%m-%d')
        filename = f"{self.village.name.lower()}_weather_{today}.csv"
        filepath = output_dir / filename

        dataframe.to_csv(filepath, index=False)
        logger.info(f"Saved full weather data to {filepath}")