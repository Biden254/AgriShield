from rest_framework import serializers
from .models import User
from django.core.validators import RegexValidator
from apps.core.models import Village   


phone_validator = RegexValidator(
    regex=r"^\+?\d{9,15}$",
    message="Enter a valid international phone number, e.g. +254712345678",
)


class UserSerializer(serializers.ModelSerializer):
    village = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ["msisdn", "name", "village", "language", "is_active", "date_joined"]
        read_only_fields = ["msisdn", "is_active", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    msisdn = serializers.CharField(validators=[phone_validator])
    name = serializers.CharField(required=False, allow_blank=True)
    village = serializers.PrimaryKeyRelatedField(
        queryset=Village.objects.all(),  
        required=False,
        allow_null=True
    )
    language = serializers.ChoiceField(
        choices=User._meta.get_field("language").choices, default="sw"
    )

    class Meta:
        model = User
        fields = ("msisdn", "name", "village", "language")

    def create(self, validated_data):
        msisdn = validated_data.pop("msisdn")
        # Create user with unusable password (OTP-based login expected)
        user = User.objects.create_user(msisdn=msisdn, **validated_data)
        return user
