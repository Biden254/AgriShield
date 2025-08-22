from rest_framework import serializers
from django.core.validators import RegexValidator
from dj_rest_auth.registration.serializers import RegisterSerializer
from apps.core.models import Village
from .models import User


# ✅ International phone validator
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


class CustomRegisterSerializer(RegisterSerializer):
    """
    Overrides dj-rest-auth's RegisterSerializer to use msisdn instead of username/email.
    """

    username = serializers.CharField(required=True, allow_blank=False, max_length=150)
    email = serializers.EmailField(required=True, allow_blank=True, allow_null=True)
    msisdn = serializers.CharField(validators=[phone_validator])
    name = serializers.CharField(required=False, allow_blank=True)
    village = serializers.PrimaryKeyRelatedField(
        queryset=Village.objects.all(), required=False, allow_null=True
    )
    language = serializers.ChoiceField(
        choices=User._meta.get_field("language").choices, default="sw"
    )

    class Meta:
        model = User
        fields = ("username", "email", "msisdn", "name", "village", "language")

    def get_cleaned_data(self):
        """
        dj-rest-auth expects this method to return the cleaned fields.
        """
        return {
            "username": self.validated_data.get("username", ""),
            "email": self.validated_data.get("email", ""),
            "msisdn": self.validated_data.get("msisdn"),
            "name": self.validated_data.get("name", ""),
            "village": self.validated_data.get("village", None),
            "language": self.validated_data.get("language", "sw"),
        }

    def save(self, request):
        """
        Override save() to create the user correctly.
        """
        user = User.objects.create_user(
            msisdn=self.validated_data["msisdn"],
            name=self.validated_data.get("name", ""),
            village=self.validated_data.get("village", None),
            language=self.validated_data.get("language", "sw"),
        )
        
        return user
