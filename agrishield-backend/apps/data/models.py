from django.db import models
from django.utils import timezone
from apps.core.models import UUIDModel  # safe to import


class Forecast(UUIDModel):
    """
    Weather forecast for a specific village.
    Stores rainfall, risk level, and raw API response.
    """
    village = models.ForeignKey(
        "core.Village",   # string reference avoids circular imports
        on_delete=models.CASCADE,
        related_name="forecasts",
    )
    rainfall = models.FloatField(default=0, help_text="Rainfall in mm")
    risk_level = models.CharField(max_length=20, default="unknown", db_index=True)
    raw = models.JSONField(default=dict, blank=True, help_text="Raw API response")
    created_at = models.DateTimeField(default=timezone.now, editable=False, db_index=True)

    class Meta:
        db_table = "data_forecast"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["risk_level"]),
            models.Index(fields=["village", "created_at"]),
        ]
        verbose_name = "Forecast"
        verbose_name_plural = "Forecasts"

    def __str__(self):
        return f"Forecast for {self.village} - {self.risk_level} ({self.created_at.date()})"
