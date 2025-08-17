"""
Fetchers package: contains all external data ingestion modules.
Only expose fetchers that are production-ready.
"""

from .openmeteo_fetcher import fetch_openmeteo_data

__all__ = [
    "fetch_openmeteo_data",
]
