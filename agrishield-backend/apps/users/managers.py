from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Manager for custom user model where msisdn (phone) is the unique identifier.
    """

    use_in_migrations = True

    def create_user(self, msisdn, password=None, **extra_fields):
        if not msisdn:
            raise ValueError(_("The msisdn must be set"))
        msisdn = self.normalize_email(msisdn) if "@" in msisdn else msisdn.strip()
        user = self.model(msisdn=msisdn, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, msisdn, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(msisdn, password, **extra_fields)
