from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from playlists.models import Playlists, PlaylistLogs
from playlists.serializers import PlaylistsSerialiser, PlaylistLogsSerialiser

class PlaylistsViewSet(viewsets.ModelViewSet):
    queryset = Playlists.objects.all()
    serializer_class = PlaylistsSerialiser
    permission_classes = [AllowAny]

class PlaylistLogsViewSet(viewsets.ModelViewSet):
    queryset = PlaylistLogs.objects.all()
    serializer_class = PlaylistLogsSerialiser
    permission_classes = [AllowAny]