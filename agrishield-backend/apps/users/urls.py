from django.urls import path
from .views import RegisterView, MeView, AdminUserListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="users-register"),
    path("me/", MeView.as_view(), name="users-me"),
    path("admin/list/", AdminUserListView.as_view(), name="users-admin-list"),
]
# This file defines the URL patterns for the users app.