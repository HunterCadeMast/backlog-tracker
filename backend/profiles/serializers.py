from rest_framework import serializers
from profiles.models import Profiles, OAuthenticationTokens, APIKeys, SteamProfiles
from games.models import Games, Developers, Publishers, Genres, Platforms, Franchises, Series

class ProfilesSerialiser(serializers.ModelSerializer):
    favorite_game = serializers.PrimaryKeyRelatedField(many = True, query_set = Games.objects.all(), required = False)
    favorite_developer = serializers.PrimaryKeyRelatedField(many = True, query_set = Developers.objects.all(), required = False)
    favorite_publisher = serializers.PrimaryKeyRelatedField(many = True, query_set = Publishers.objects.all(), required = False)
    favorite_genre = serializers.PrimaryKeyRelatedField(many = True, query_set = Genres.objects.all(), required = False)
    favorite_platform = serializers.PrimaryKeyRelatedField(many = True, query_set = Platforms.objects.all(), required = False)
    favorite_franchise = serializers.PrimaryKeyRelatedField(many = True, query_set = Franchises.objects.all(), required = False)
    favorite_series = serializers.PrimaryKeyRelatedField(many = True, query_set = Series.objects.all(), required = False)

    class Meta:
        model = Profiles
        fields = ['id', 'user', 'display_name', 'profile_photo', 'private_profile', 'website_theme', 'bio', 'favorite_game', 'favorite_developer', 'favorite_publisher', 'favorite_genre', 'favorite_platform', 'favorite_franchise', 'favorite_series', 'playstyle']
        read_only_fields = ['id', 'user']

class OAuthenticationTokensSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OAuthenticationTokens
        fields = ['id', 'profile_id', 'provider_id', 'user', 'provider_name', 'access_token', 'refresh_token', 'creation_timestamp', 'expiration_date']
        read_only_fields = ['id', 'profile_id', 'provider_id', 'user', 'provider_name', 'creation_timestamp']
        extra_kwargs = {
            'access_token': {'write_only': True},
            'refresh_token': {'write_only': True}
        }

class APIKeysSerialiser(serializers.ModelSerializer):
    class Meta:
        model = APIKeys
        fields = ['id', 'profile_id', 'user', 'api_token', 'creation_timestamp', 'last_fetched']
        read_only_fields = ['id', 'profile_id', 'user', 'creation_timestamp', 'last_fetched']
        extra_kwargs = {
            'api_token': {'write_only': True}
        }

class SteamProfilesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = SteamProfiles
        fields = ['id', 'steam_id', 'user', 'steam_username', 'steam_avatar_link', 'steam_public_profile', 'auto_sync_playtime', 'auto_sync_games', 'creation_timestamp', 'last_fetched']
        read_only_fields = ['id', 'steam_id', 'user', 'steam_username', 'steam_avatar_link', 'steam_public_profile', 'auto_sync_playtime', 'auto_sync_games', 'creation_timestamp', 'last_fetched']