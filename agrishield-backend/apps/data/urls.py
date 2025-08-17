from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FloodIndicatorViewSet

router = DefaultRouter()
router.register(r'flood-indicators', FloodIndicatorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]