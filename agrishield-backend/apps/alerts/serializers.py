from rest_framework import serializers
from .models import Alert, AlertDelivery
from apps.core.models import Village, Farmer
from apps.core.serializers import VillageSerializer
from django.conf import settings

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ["id", "name", "location"]


class FarmerSerializer(serializers.ModelSerializer):
   from apps.users.models import Farmer
   class Meta:
        model = Farmer
        fields = ["id", "name", "phone_number", "preferred_language"]


class AlertSerializer(serializers.ModelSerializer):
    village = VillageSerializer(read_only=True)
    village_id = serializers.PrimaryKeyRelatedField(
        queryset=Village.objects.all(), source="village", write_only=True
    )

    generated_message = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = [
           "id",
            "village",
            "village_id",
            "alert_level",
            "message",
            "generated_message",
            "triggered_at",
            "valid_until",
            "is_active",
            "acknowledged",
            "rainfall_data",
            "river_level",
            "indigenous_indicators",
       ]
        read_only_fields = ["triggered_at"]

    def get_generated_message(self, obj):
        return obj.generate_message()


class AlertDeliverySerializer(serializers.ModelSerializer):
    alert = AlertSerializer(read_only=True)
    alert_id = serializers.PrimaryKeyRelatedField(
        queryset=Alert.objects.all(), source="alert", write_only=True
    )

    farmer = FarmerSerializer(read_only=True)
    farmer_id = serializers.PrimaryKeyRelatedField(
        queryset=Farmer.objects.all(), source="farmer", write_only=True
    )

    class Meta:
        model = AlertDelivery
        fields = [
            "id",
            "alert",
            "alert_id",
            "farmer",
           "farmer_id",
            "delivery_method",
            "status",
            "sent_at",
            "delivery_confirmed",
        ]
        read_only_fields = ["sent_at", "status", "delivery_confirmed"]
