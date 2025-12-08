from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAccountOwner
from steam.models import SteamProfiles
from steam.serializers import SteamProfilesSerializer

class SteamProfilesViewSet(viewsets.ModelViewSet):
    serializer_class = SteamProfilesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return SteamProfiles.objects.filter(user = self.request.user)
