from rest_framework import permissions


class IsFarmerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access for everyone, but write access only to authenticated Farmers.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow if user has a Farmer profile
        return request.user.is_authenticated and hasattr(request.user, "farmer")


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access for everyone, but write access only to admins/staff.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission: allow read-only for everyone,
    but write access only for the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsFarmer(permissions.BasePermission):
    """
    Allow access only if the user is a Farmer.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "farmer")
