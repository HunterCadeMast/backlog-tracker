from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'user', None) == request.user or getattr(obj, 'owner', None) == request.user
    
class APIKeyAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return (IsAuthenticated().has_permission(request, view) or HasAPIKey().has_permission(request, view))