from django.db import models
from apps.core.models import Village
from django.conf import settings


class Alert(models.Model):
    ALERT_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MODERATE', 'Moderate Risk'),
        ('HIGH', 'High Risk'),
        ('CRITICAL', 'Critical Emergency'),
    ]

    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name="alerts")
    alert_level = models.CharField(max_length=20, choices=ALERT_LEVELS)
    message = models.TextField(blank=True)  # can be auto-generated
    triggered_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    acknowledged = models.BooleanField(default=False)  # added for lifecycle tracking

    # Scientific data references
    rainfall_data = models.JSONField(null=True, blank=True)
    river_level = models.FloatField(null=True, blank=True)

    # Indigenous knowledge references
    indigenous_indicators = models.JSONField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["village", "is_active"]),
            models.Index(fields=["alert_level", "valid_until"]),
        ]
        ordering = ["-triggered_at"]

    def __str__(self):
        return f"{self.village.name} - {self.alert_level} Alert"

    def generate_message(self):
        """
        Generate localized alert message with actionable steps.
        If message was manually set, return that instead.
        """
        if self.message:
            return self.message

        base_msg = f"[{self.alert_level}] {self.village.name}: "

        if self.alert_level == "CRITICAL":
            actions = "Immediate evacuation required! Move to designated safe zones."
            indicators = ""
            if self.indigenous_indicators:
                indicators = " Locals report: " + ", ".join(self.indigenous_indicators.values())
            return base_msg + f"Severe flooding imminent. {actions}{indicators}"

        elif self.alert_level == "HIGH":
            actions = "Harvest crops NOW. Move livestock to higher ground. Prepare to evacuate."
            indicators = ""
            if self.indigenous_indicators:
                indicators = " Locals report: " + ", ".join(self.indigenous_indicators.values())
            return base_msg + f"Flood expected within 48 hours. {actions}{indicators}"

        elif self.alert_level == "MODERATE":
            return base_msg + "Possible flood in 3–5 days. Prepare your farm."

        return base_msg + "No immediate flood risk. Stay alert."


class AlertDelivery(models.Model):
    DELIVERY_METHODS = [
        ("SMS", "SMS"),
        ("USSD", "USSD"),
    ]

    DELIVERY_STATUS = [
        ("PENDING", "Pending"),
        ("SENT", "Sent"),
        ("FAILED", "Failed"),
        ("DELIVERED", "Delivered"),
    ]

    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name="deliveries")
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHODS)
    status = models.CharField(max_length=10, choices=DELIVERY_STATUS, default="PENDING")
    sent_at = models.DateTimeField(null=True, blank=True)
    delivery_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("alert", "farmer")
        indexes = [
            models.Index(fields=["status", "sent_at"]),
        ]

    def __str__(self):
        return f"{self.farmer.phone_number} - {self.alert.alert_level} ({self.status})"
