from django.urls import path
from . import views

urlpatterns = [
    path("entry/", views.ussd_callback, name="ussd-entry"),
]
