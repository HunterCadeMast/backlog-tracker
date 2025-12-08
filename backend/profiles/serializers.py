from rest_framework import serializers
from profiles.models import Profiles, OAuthenticationTokens, APIKeys
from games.models import Games, Developers, Publishers, Genres, Platforms, Franchises, Series

class ProfilesSerializer(serializers.ModelSerializer):
    favorite_game = serializers.PrimaryKeyRelatedField(many = True, queryset = Games.objects.all(), required = False)
    favorite_developer = serializers.PrimaryKeyRelatedField(many = True, queryset = Developers.objects.all(), required = False)
    favorite_publisher = serializers.PrimaryKeyRelatedField(many = True, queryset = Publishers.objects.all(), required = False)
    favorite_genre = serializers.PrimaryKeyRelatedField(many = True, queryset = Genres.objects.all(), required = False)
    favorite_platform = serializers.PrimaryKeyRelatedField(many = True, queryset = Platforms.objects.all(), required = False)
    favorite_franchise = serializers.PrimaryKeyRelatedField(many = True, queryset = Franchises.objects.all(), required = False)
    favorite_series = serializers.PrimaryKeyRelatedField(many = True, queryset = Series.objects.all(), required = False)

    class Meta:
        model = Profiles
        fields = ['id', 'user', 'display_name', 'profile_photo', 'private_profile', 'website_theme', 'bio', 'favorite_game', 'favorite_developer', 'favorite_publisher', 'favorite_genre', 'favorite_platform', 'favorite_franchise', 'favorite_series', 'playstyle']
        read_only_fields = ['id', 'user']

class OAuthenticationTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAuthenticationTokens
        fields = ['id', 'profile_id', 'provider_id', 'user', 'provider_name', 'access_token', 'refresh_token', 'creation_timestamp', 'expiration_date']
        read_only_fields = ['id', 'profile_id', 'provider_id', 'user', 'provider_name', 'creation_timestamp']
        extra_kwargs = {
            'access_token': {'write_only': True},
            'refresh_token': {'write_only': True}
        }

class APIKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKeys
        fields = ['id', 'profile_id', 'user', 'api_token', 'creation_timestamp', 'last_fetched']
        read_only_fields = ['id', 'profile_id', 'user', 'creation_timestamp', 'last_fetched']
        extra_kwargs = {
            'api_token': {'write_only': True}
        }