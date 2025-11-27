from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'user', None) == request.user or getattr(obj, 'owner', None) == request.user