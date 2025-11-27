from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAccountOwner
from playlists.models import Playlists, PlaylistLogs
from playlists.serializers import PlaylistsSerialiser, PlaylistLogsSerialiser

class PlaylistsViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return Playlists.objects.filter(user = self.request.user)

class PlaylistLogsViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistLogsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return PlaylistLogs.objects.filter(user = self.request.user)