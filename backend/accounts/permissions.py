from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.utils import timezone
from profiles.models import APIKeys

class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'user', None) == request.user or getattr(obj, 'owner', None) == request.user
    
class APIKeyAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if IsAuthenticated().has_permission(request, view):
            return True
        else:
            api_key_check = HasAPIKey()
            if not api_key_check.has_permission(request, view):
                return False
            raw_api_key = request.headers.get('Authorization')
            if not raw_api_key:
                return False
            split_key = raw_api_key.split()
            if len(split_key) != 2:
                return False
            api_key_prefix = split_key[1][:8]
            try:
                api_key = APIKeys.objects.get(api_token = api_key_prefix)
            except APIKeys.DoesNotExist:
                return False
            api_key.last_fetched = timezone.now()
            api_key.save(update_fields = ['last_fetched'])
            return True