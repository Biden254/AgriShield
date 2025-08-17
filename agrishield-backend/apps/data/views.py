from rest_framework import viewsets, permissions
from .models import Forecast
from .serializers import FloodIndicatorSerializer

class FloodIndicatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows flood indicators to be viewed or edited.
    """
    queryset = Forecast.objects.all().select_related('village').order_by('created_at')
    serializer_class = FloodIndicatorSerializer
    permission_classes = [permissions.IsAuthenticated] # Or IsAuthenticatedOrReadOnly
    filterset_fields = ['village', 'risk_level']

    # You can add more complex filtering or custom actions here if needed.