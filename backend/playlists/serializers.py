from rest_framework import serializers
from playlists.models import Playlists, PlaylistLogs

class PlaylistsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Playlists
        fields = ['id', 'user', 'profile_id', 'playlist_title', 'creation_timestamp', 'updated_timestamp']
        read_only_fields = ['id', 'user', 'profile_id', 'creation_timestamp']

class PlaylistLogsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = PlaylistLogs
        fields = ['id', 'user', 'playlist_id', 'log_id', 'current_position']
        read_only_fields = ['id', 'user', 'playlist_id', 'log_id']