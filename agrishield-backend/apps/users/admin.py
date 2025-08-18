from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User, Farmer


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show Farmer profiles if role is 'farmer'
        if self.instance and self.instance.role != "farmer":
            self.fields["farmer_profile"].queryset = Farmer.objects.none()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminForm

    ordering = ("msisdn",)
    list_display = (
        "msisdn",
        "get_name",
        "role",
        "farmer_village",
        "language",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = ("role", "is_staff", "is_active", "language")
    search_fields = ("msisdn", "get_name")

    fieldsets = (
        (None, {"fields": ("msisdn", "password")}),
        (_("Personal info"), {"fields": ("role", "farmer_profile", "language")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("msisdn", "password1", "password2", "role", "farmer_profile", "is_staff", "is_active"),
        }),
    )

    def get_name(self, obj):
        return obj.farmer_profile.name if obj.farmer_profile else "-"
    get_name.short_description = "Name"

    def farmer_village(self, obj):
        return obj.farmer_profile.village.name if obj.farmer_profile and obj.farmer_profile.village else "-"
    farmer_village.short_description = "Village"

    # Only assign Farmer profile if role is farmer and admin selected a profile
    def save_model(self, request, obj, form, change):
        if obj.role == "farmer" and not obj.farmer_profile:
            # Optionally auto-create a minimal Farmer profile if none selected
            farmer = Farmer.objects.create(name=obj.msisdn)
            obj.farmer_profile = farmer
        elif obj.role != "farmer":
            obj.farmer_profile = None  # Clear Farmer profile for other roles
        super().save_model(request, obj, form, change)
