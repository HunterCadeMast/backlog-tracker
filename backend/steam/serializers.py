from rest_framework import serializers
from steam.models import SteamProfiles

class SteamProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamProfiles
        fields = ['id', 'steam_id', 'user', 'steam_username', 'steam_avatar_link', 'steam_public_profile', 'auto_sync_playtime', 'auto_sync_games', 'creation_timestamp', 'last_fetched']
        read_only_fields = ['id', 'steam_id', 'user', 'steam_username', 'steam_avatar_link', 'steam_public_profile', 'auto_sync_playtime', 'auto_sync_games', 'creation_timestamp', 'last_fetched']