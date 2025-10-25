from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow access only to the object's owner or admin users."""

    def has_object_permission(self, request, view, obj):
        # obj expected to be a User instance
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_staff or obj == request.user
