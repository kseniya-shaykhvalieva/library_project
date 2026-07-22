from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Если пользователь является владельцем"""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
