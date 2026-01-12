from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from profiles.models import Profiles

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False
    
    def add_message(self, request, level, message_template, message_context = None, extra_tags = ''):
        pass

    def get_login_redirect_url(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        return f"{settings.FRONTEND_URL}/oauthentication/callback/?access={str(refresh.access_token)}&refresh={str(refresh)}"

class AllAuthAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin = None):
        return True

    def is_auto_signup_allowed(self, request, sociallogin):
        return True

    def save_user(self, request, sociallogin, form = None):
        user = super().save_user(request, sociallogin, form)
        Profiles.objects.get_or_create(user = user, defaults = {'display_name': user.username, 'private_profile': False,},)
        return user
    
    def get_login_redirect_url(self, request, socialaccount = None):
        user = request.user
        if not user.is_authenticated and socialaccount:
            user = socialaccount.user
        refresh = RefreshToken.for_user(user)
        return f"{settings.FRONTEND_URL}/oauthentication/callback/?access={str(refresh.access_token)}&refresh={str(refresh)}"