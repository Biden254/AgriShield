from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Import Village model — adjust path if your Village lives elsewhere
try:
    from apps.core.models import Village
except Exception:
    Village = None  # Stay import-safe; replace import if needed in your codebase


LANGUAGE_CHOICES = [
    ("sw", "Kiswahili"),
    ("en", "English"),
    # add local dialect codes as needed
]

class Farmer(models.Model):
    """
    Farmer profile information.
    """
    name = models.CharField(max_length=128, blank=True, null=True)
    village = models.ForeignKey(
        "core.Village",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="farmers",
    )
    preferred_language = models.CharField(max_length=8, choices=LANGUAGE_CHOICES, default="sw")


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user where MSISDN (phone number) is the unique identifier.
    Suitable for an SMS-first system.
    """
    msisdn = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        help_text=_("Mobile phone number in international format, e.g. +2547..."),
    )
    farmer_profile = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True,
        related_name="users",
    )
    language = models.CharField(max_length=8, choices=LANGUAGE_CHOICES, default="sw")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "msisdn"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users_user"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.name or self.msisdn} ({self.msisdn})"
