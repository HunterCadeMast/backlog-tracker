from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.permissions import IsAccountOwner
from profiles.models import Profiles, OAuthenticationTokens, APIKeys, SteamProfiles
from profiles.serializers import ProfilesSerialiser, OAuthenticationTokensSerialiser, APIKeysSerialiser, SteamProfilesSerialiser

class ProfilesViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilesSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        return Profiles.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    @action(detail = True, methods = ['patch'])
    def update_profile_photo(self, request, pk = None):
        profile = self.get_object()
        profile_photo = request.FILES.get('profile_photo')
        if not profile_photo:
            return Response({'error': 'No profile photo found!'}, status = 400)
        profile.profile_photo = profile_photo
        profile.save()
        return Response({'message': 'Profile photo updated!'})
    
    @action(detail = True, methods = ['patch'])
    def toggle_visibility(self, request, pk = None):
        profile = self.get_object()
        profile.private_profile = not profile.private_profile
        profile.save()
        return Response({'message': 'Profile visibility inverted!'}, status = 200)
    
    @action(detail = True, methods = ['patch'])
    def change_profile_info(self, request, pk = None):
        profile = self.get_object()
        profile_serializer = self.get_serializer(profile, data = request.data, partial = True)
        profile_serializer.is_valid(raise_exception = True)
        profile_serializer.save()
        return Response({'message': 'Updated profile!'}, status = 200)

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