from rest_framework import serializers
from .models import Village



class VillageSerializer(serializers.ModelSerializer):
    """
    Serializer for Village model.
    Exposes village basic information along with computed risk level.
    """

    risk_level_display = serializers.SerializerMethodField()

    class Meta:
        model = Village
        fields = [
            "id",
            "name",
            "risk_level",          # raw enum/choice field
            "risk_level_display",  # human-readable label
        ]
        read_only_fields = ["risk_level", "risk_level_display"]

    def get_risk_level_display(self, obj):
        """
        Returns human-friendly risk level (e.g., LOW -> 'Low Risk').
        """
        return obj.get_risk_level_display() if hasattr(obj, "get_risk_level_display") else obj.risk_level
