from django.urls import path
from .views import SendSMSView, sms_health_check

urlpatterns = [
    path("send/", SendSMSView.as_view(), name="send_sms"),
    path("health/", sms_health_check, name="sms_health_check"),
]
