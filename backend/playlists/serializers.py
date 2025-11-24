from rest_framework import serializers
from playlists.models import Playlists, PlaylistLogs

class PlaylistsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Playlists
        fields = ['id', 'profile_id', 'playlist_title', 'creation_timestamp']
        read_only_fields = ['id', 'profile_id', 'creation_timestamp']

class PlaylistLogsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = PlaylistLogs
        fields = ['id', 'playlist_id', 'log_id', 'ordered_playlist_position']
        read_only_fields = ['id', 'playlist_id', 'log_id']