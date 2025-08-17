"""
Utility functions for the data app.
"""

from datetime import datetime

def parse_timestamp(ts: str) -> datetime:
    """
    Parse ISO timestamp string to datetime object.
    """
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return datetime.utcnow()

def mm_to_inches(mm: float) -> float:
    """
    Convert millimeters of rainfall to inches.
    """
    return round(mm / 25.4, 2)
