from rest_framework import serializers
from profiles.models import Profiles, APIKeys
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

class APIKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKeys
        fields = ['id', 'user', 'api_token_prefix', 'creation_timestamp', 'last_fetched', 'rotate', 'expiration_date', 'expired']
        read_only_fields = ['id', 'user', 'api_token_prefix', 'creation_timestamp', 'last_fetched', 'rotate', 'expiration_date']