from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from profiles.models import Profiles, OAuthenticationTokens, APIKeys, SteamProfiles
from profiles.serializers import ProfilesSerialiser, OAuthenticationTokensSerialiser, APIKeysSerialiser, SteamProfilesSerialiser

class ProfilesViewSet(viewsets.ModelViewSet):
    queryset = Profiles.objects.all()
    serializer_class = ProfilesSerialiser
    permission_classes = [AllowAny]

class OAuthenticationTokensViewSet(viewsets.ModelViewSet):
    queryset = OAuthenticationTokens.objects.all()
    serializer_class = OAuthenticationTokensSerialiser
    permission_classes = [AllowAny]

class APIKeysViewSet(viewsets.ModelViewSet):
    queryset = APIKeys.objects.all()
    serializer_class = APIKeysSerialiser
    permission_classes = [AllowAny]

class SteamProfilesViewSet(viewsets.ModelViewSet):
    queryset = SteamProfiles.objects.all()
    serializer_class = SteamProfilesSerialiser
    permission_classes = [AllowAny]