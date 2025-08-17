from rest_framework import serializers
from .models import Forecast
from apps.core.serializers import VillageSerializer

class FloodIndicatorSerializer(serializers.ModelSerializer):
    # Use a nested serializer for a richer, more structured API output.
    village = VillageSerializer(read_only=True)

    class Meta:
        model = Forecast
        # The fields list is now cleaner and more intuitive.
        fields = ['id', 'village', 'rainfall', 'risk_level', 'created_at']