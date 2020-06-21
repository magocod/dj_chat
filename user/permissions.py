"""
Permisos
"""

from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Superusuario
    """

    def has_permission(self, request, view):
        """
        ...
        """
        return bool(request.user and request.user.is_superuser)
