from rest_framework.throttling import SimpleRateThrottle
from django.utils import timezone
from profiles.models import APIKeys

class RegisterThrottle(SimpleRateThrottle):
    scope = 'register'

    def get_cache_key(self, request, view):
        return self.get_ident(request)

class LoginThrottle(SimpleRateThrottle):
    scope = 'login'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None
        return self.get_ident(request)
    
class PasswordResetThrottle(SimpleRateThrottle):
    scope = 'password_reset'

    def get_cache_key(self, request, view):
        return self.get_ident(request)

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