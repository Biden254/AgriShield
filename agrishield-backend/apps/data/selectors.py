from django.db.models import Avg, Max, Min
from apps.data.models import FloodIndicator
from django.utils import timezone

def get_latest_river_level(village):
    return FloodIndicator.objects.filter(
        village=village, indicator_type="RIVER_LEVEL"
    ).order_by("-created_at").first()

def get_latest_rainfall(village):
    return FloodIndicator.objects.filter(
        village=village, indicator_type="RAINFALL"
    ).order_by("-created_at").first()

def get_avg_rainfall(village, days=7):
    return (
        FloodIndicator.objects.filter(
            village=village, indicator_type="RAINFALL", 
            created_at__gte=timezone.now() - timezone.timedelta(days=days)
        ).aggregate(avg=Avg("value"))["avg"]
    )

def get_max_river_level(village, days=7):
    return (
        FloodIndicator.objects.filter(
            village=village, indicator_type="RIVER_LEVEL", 
            created_at__gte=timezone.now() - timezone.timedelta(days=days)
        ).aggregate(max=Max("value"))["max"]
    )
