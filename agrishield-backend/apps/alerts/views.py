from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from apps.alerts.models import Alert, AlertDelivery
from apps.alerts.serializers import AlertSerializer, AlertDeliverySerializer
from apps.users.permissions import IsFarmerOrReadOnly, IsAdminOrReadOnly


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing alerts"""
    queryset = Alert.objects.filter(is_active=True).select_related('village')
    serializer_class = AlertSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['village', 'alert_level']
    ordering = ['-triggered_at']
    permission_classes = [IsFarmerOrReadOnly]   # 👈 Farmers can confirm, others read-only

    @action(detail=True, methods=['post'], permission_classes=[IsFarmerOrReadOnly])
    def confirm_receipt(self, request, pk=None):
        """Allow farmers to confirm they received an alert"""
        alert = self.get_object()
        farmer = request.user

        delivery, created = AlertDelivery.objects.get_or_create(
            alert=alert,
            farmer=farmer,
            defaults={
                'delivery_method': 'APP',
                'status': 'DELIVERED',
                'delivery_confirmed': True
            }
        )

        if not created and not delivery.delivery_confirmed:
            delivery.delivery_confirmed = True
            delivery.save()

        return Response({'status': 'confirmed'})


class AlertDeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for alert delivery tracking"""
    serializer_class = AlertDeliverySerializer
    permission_classes = [IsFarmerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:   # 👈 Staff/admins can see all deliveries
            return AlertDelivery.objects.all().select_related('alert', 'farmer')
        return AlertDelivery.objects.filter(
            farmer=self.request.user.farmer
        ).select_related('alert')
