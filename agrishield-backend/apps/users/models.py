from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Import Village model safely
try:
    from apps.core.models import Village
except ImportError:
    Village = None

LANGUAGE_CHOICES = [
    ("sw", "Kiswahili"),
    ("en", "English"),
]

ROLE_CHOICES = [
    ("farmer", "Farmer"),
    ("fisher", "Fisher"),
    ("government", "Government Official"),
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
    preferred_language = models.CharField(
        max_length=8,
        choices=LANGUAGE_CHOICES,
        default="sw",
    )

    def __str__(self):
        return self.name or f"Farmer {self.id}"


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user supporting:
    - Email + password for app/web users.
    - MSISDN for USSD users.
    """

    # ✅ Email for frontend users (unique but optional if MSISDN is used instead)
    email = models.EmailField(
        _("email address"),
        unique=True,
        null=True,
        blank=True,
    )

    # ✅ MSISDN for USSD-based login (unique but optional if email is used instead)
    msisdn = models.CharField(
        max_length=32,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("Mobile phone number in international format, e.g. +2547..."),
    )

    farmer_profile = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="farmer",
    )
    language = models.CharField(
        max_length=8,
        choices=LANGUAGE_CHOICES,
        default="sw",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    # ✅ Allow login via email OR msisdn
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["msisdn"]  # Still collect phone number for USSD users

    class Meta:
        db_table = "users_user"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        if self.email:
            return self.email
        return self.msisdn or f"User {self.id}"
