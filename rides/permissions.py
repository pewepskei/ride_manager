from rest_framework import permissions

class IsAdminUserRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        return getattr(user, 'role', None) == 'admin'
