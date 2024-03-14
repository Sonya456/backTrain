from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated


class IsOwnerOrAdmin(permissions.BasePermission):
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny] 
        elif self.action in ['create', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated] 
        return [permission() for permission in permission_classes]



class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the admin user.
        return request.user and request.user.is_staff
