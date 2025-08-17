from django.urls import path, include

urlpatterns = [
    path("sms/", include("apps.integrations.sms.urls")),
    path("ussd/", include("apps.integrations.ussd.urls")),
]
