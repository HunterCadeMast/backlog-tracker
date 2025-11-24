from rest_framework import serializers
from profiles.models import Profiles, OAuthenticationTokens, APIKeys, SteamProfiles

class ProfilesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['id', 'username', 'email', 'hashed_password', 'creation_timestamp']
        read_only_fields = ['id', 'creation_timestamp']
        extra_kwargs = {
            'hashed_password': {'write_only': True}
        }

class OAuthenticationTokensSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OAuthenticationTokens
        fields = ['id', 'profile_id', 'provider_id', 'provider_name', 'access_token', 'refresh_token', 'creation_timestamp', 'expiration_date']
        read_only_fields = ['id', 'profile_id', 'provider_id', 'provider_name', 'creation_timestamp']
        extra_kwargs = {
            'access_token': {'write_only': True},
            'refresh_token': {'write_only': True}
        }

class APIKeysSerialiser(serializers.ModelSerializer):
    class Meta:
        model = APIKeys
        fields = ['id', 'profile_id', 'api_token', 'creation_timestamp', 'last_fetched']
        read_only_fields = ['id', 'profile_id', 'creation_timestamp', 'last_fetched']
        extra_kwargs = {
            'api_token': {'write_only': True}
        }

class SteamProfilesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = SteamProfiles
        fields = ['id', 'steam_id', 'steam_username', 'steam_avatar_link', 'creation_timestamp', 'last_fetched']
        read_only_fields = ['id', 'steam_id', 'steam_username', 'steam_avatar_link', 'creation_timestamp', 'last_fetched']