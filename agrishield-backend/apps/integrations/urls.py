from django.urls import path
from .views import ussd_callback

app_name = "integrations"
urlpatterns = [
    path("ussd/", ussd_callback, name="ussd_callback"),
]