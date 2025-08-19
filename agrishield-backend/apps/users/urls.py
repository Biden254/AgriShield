# users/urls.py
from django.urls import path
from .views import RegisterView, MeView, AdminUserListView, FarmerProfileView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="users-register"),
    path("me/", MeView.as_view(), name="users-me"),
    path("farmer/", FarmerProfileView.as_view(), name="users-farmer"),
    path("admin/list/", AdminUserListView.as_view(), name="users-admin-list"),
]
