from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("msisdn",)
    list_display = (
        "msisdn",
        "farmer_name",
        "farmer_village",
        "language",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_staff", "is_active", "language")
    search_fields = ("msisdn", "farmer_name")

    fieldsets = (
        (None, {"fields": ("msisdn", "password")}),
        (_("Personal info"), {"fields": ("farmer_profile", "language")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("msisdn", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    # Custom display functions for related Farmer fields
    def farmer_name(self, obj):
        return obj.farmer_profile.name if obj.farmer_profile else "-"
    farmer_name.short_description = "Name"

    def farmer_village(self, obj):
        return obj.farmer_profile.village.name if obj.farmer_profile and obj.farmer_profile.village else "-"
    farmer_village.short_description = "Village"
