from rest_framework import serializers
from accounts.models import CustomUser
from profiles.models import Profiles, OAuthenticationTokens, APIKeys, SteamProfiles

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'creation_timestamp']
        read_only_fields = ['id', 'creation_timestamp']
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def create(self, validated_data):
            user = CustomUser(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user

class ProfilesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['user', 'profile_photo', 'bio']
        read_only_fields = ['user']

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
        fields = ['id', 'steam_id', 'user', 'steam_username', 'steam_avatar_link', 'creation_timestamp', 'last_fetched']
        read_only_fields = ['id', 'steam_id', 'user', 'steam_username', 'steam_avatar_link', 'creation_timestamp', 'last_fetched']