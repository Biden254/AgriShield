from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom manager to handle both email+password login (frontend) 
    and msisdn-only registration (USSD users).
    """

    use_in_migrations = True

    def create_user(self, email=None, msisdn=None, password=None, **extra_fields):
        """
        Create and save a User with either email OR msisdn.
        - If email is provided, normalize and use it.
        - If only msisdn is provided, it's treated as USSD-only user.
        """

        if not email and not msisdn:
            raise ValueError(_("You must provide either an email or an MSISDN"))

        # ✅ Normalize email if provided
        if email:
            email = self.normalize_email(email)
        else:
            email = None

        # ✅ Clean up msisdn if provided
        if msisdn:
            msisdn = msisdn.strip()
        else:
            msisdn = None

        user = self.model(email=email, msisdn=msisdn, **extra_fields)

        # ✅ Password is required for email-based accounts, but optional for USSD
        if password:
            user.set_password(password)
        elif email:
            raise ValueError(_("Password is required when registering via email"))
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser using email + password.
        Superusers **must** have email and password.
        """
        if not email:
            raise ValueError(_("Superuser must have an email address"))
        if not password:
            raise ValueError(_("Superuser must have a password"))

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email=email, password=password, **extra_fields)
