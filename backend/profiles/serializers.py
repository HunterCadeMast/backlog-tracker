from rest_framework import serializers
from django.db.models import Sum
from collections import defaultdict
from profiles.models import Profiles, APIKeys
from games.models import Games, Developers, Publishers, Genres, Platforms, Franchises, Series
from logs.models import Logs

class ProfileStatisticsMixin:
    def get_statistics(self, profile):
        logs = Logs.objects.filter(user = profile.user)
        completed_games = logs.filter(user_status = 'completed')
        yearly_games = defaultdict(int)
        for log in completed_games.exclude(completion_date = None):
            year = log.completion_date.year
            yearly_games[year] = yearly_games.get(year, 0) + 1
        data = {'total_games': logs.count(), 'completed_games': completed_games.count(), 'total_playtime': logs.aggregate(total = Sum('user_playtime'))['total'] or 0, 'yearly_completed_games': dict(yearly_games), 'favorite_genres': list(profile.favorite_genre.values_list('label', flat = True)),}
        return data

class ProfilesSerializer(ProfileStatisticsMixin, serializers.ModelSerializer):
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = Profiles
        fields = ['id', 'user', 'display_name', 'profile_photo', 'private_profile', 'website_theme', 'bio', 'favorite_game', 'favorite_developer', 'favorite_publisher', 'favorite_genre', 'favorite_platform', 'favorite_franchise', 'favorite_series', 'playstyle', 'statistics']
        read_only_fields = ['id', 'user']

    def get_statistics(self, obj):
        return self.get_statistics(obj)

class UsersSerializer(ProfileStatisticsMixin, serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username')
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = Profiles
        fields = ['username', 'profile_photo', 'bio', 'statistics']

    def get_statistics(self, obj):
        return self.get_statistics(obj)

class APIKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKeys
        fields = ['id', 'user', 'api_token_prefix', 'creation_timestamp', 'last_fetched', 'rotate', 'expiration_date', 'expired']
        read_only_fields = ['id', 'user', 'api_token_prefix', 'creation_timestamp', 'last_fetched', 'rotate', 'expiration_date']