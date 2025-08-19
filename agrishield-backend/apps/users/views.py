# users/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from .permissions import IsFarmerOrReadOnly


class RegisterView(generics.CreateAPIView):
    """
    Register a new user by MSISDN.
    Expected payload:
      { "msisdn": "+2547...", "name": "Peter", "village": <id>, "language": "sw" }
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"detail": "registered", "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED
        )


class MeView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the current user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class FarmerProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated farmer’s profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsFarmerOrReadOnly]

    def get_object(self):
        return self.request.user.farmer


class AdminUserListView(generics.ListAPIView):
    """
    Admin-only: list all users.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.select_related("village").all()
