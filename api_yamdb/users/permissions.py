from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение администратора."""
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin:
            return True
