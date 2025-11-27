from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAccountOwner
from profiles.models import Profiles, OAuthenticationTokens, APIKeys, SteamProfiles
from profiles.serializers import ProfilesSerialiser, OAuthenticationTokensSerialiser, APIKeysSerialiser, SteamProfilesSerialiser

class ProfilesViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilesSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return Profiles.objects.filter(user = self.request.user)

class OAuthenticationTokensViewSet(viewsets.ModelViewSet):
    serializer_class = OAuthenticationTokensSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return OAuthenticationTokens.objects.filter(user = self.request.user)

class APIKeysViewSet(viewsets.ModelViewSet):
    serializer_class = APIKeysSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return APIKeys.objects.filter(user = self.request.user)

class SteamProfilesViewSet(viewsets.ModelViewSet):
    serializer_class = SteamProfilesSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return SteamProfiles.objects.filter(user = self.request.user)