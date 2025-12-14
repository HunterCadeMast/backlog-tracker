from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.throttling import SimpleRateThrottle
from django.utils import timezone
from profiles.models import APIKeys

class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'user', None) == request.user or getattr(obj, 'owner', None) == request.user
    
class APIKeyAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if IsAuthenticated().has_permission(request, view):
            return True
        elif not HasAPIKey().has_permission(request, view):
            return False
        else:
            api_key_check = request.META.get('HTTP_AUTHORIZATION', '')
            api_key_split = api_key_check.split()
            if len(api_key_split) == 2:
                api_key_full = api_key_split[1]
            else:
                api_key_full = request.META.get('HTTP_API_KEY', None)
            if not api_key_full:
                return False
            api_key_prefix = api_key_full[:8]
            try:
                api_key_model = APIKeys.objects.get(api_key_prefix = api_key_prefix, expired = False)
                api_key_model.last_fetched = timezone.now()
                api_key_model.save(update_fields = ['last_fetched'])
                if api_key_model.expired:
                    return False
                elif api_key_model.expiration_date < timezone.now():
                    api_key_model.expired = True
                    api_key_model.save(update_fields = ['expired'])
                    return False
                else:
                    return True
            except APIKeys.DoesNotExist:
                return False
            
class APIKeyThrottle(SimpleRateThrottle):
    scope = 'api_key'

    def get_cache_key(self, request, view):
        api_key = request.META.get('HTTP_AUTHORIZATION', '')
        if not api_key.startswith('api-key '):
            return None
        api_key_prefix = api_key.split()[1][:8]
        if not APIKeys.objects.filter(api_key_prefix = api_key_prefix, expired = False, expiration_date__gt = timezone.now()).exists():
            return None
        return f'api_key_{api_key_prefix}'