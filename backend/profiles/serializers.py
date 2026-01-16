from rest_framework import serializers
from django.db.models import Sum
from collections import defaultdict
from profiles.models import Profiles, APIKeys
from games.models import Games
from logs.models import Logs

class ProfileStatisticsMixin:
    def statistics(self, profile):
        logs = Logs.objects.filter(user = profile.user)
        completed_games = logs.filter(user_status = 'completed')
        playing_games = logs.filter(user_status = 'playing')
        backlog_games = logs.filter(user_status = 'backlog')
        dropped_games = logs.filter(user_status = 'dropped')
        paused_games = logs.filter(user_status = 'paused')
        yearly_games = defaultdict(int)
        for log in completed_games.exclude(completion_date = None):
            year = log.completion_date.year
            yearly_games[year] = yearly_games.get(year, 0) + 1
        data = {'total_games': logs.count(), 'completed_games': completed_games.count(), 'playing_games': playing_games.count(), 'backlog_games': backlog_games.count(), 'dropped_games': dropped_games.count(), 'paused_games': paused_games.count(), 'total_playtime': logs.aggregate(total = Sum('user_playtime'))['total'] or 0, 'yearly_completed_games': dict(yearly_games), 'favorite_genres': list(profile.favorite_genre.values_list('label', flat = True)),}
        return data
    
class FavoriteGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'igdb_id', 'game_title', 'cover_artwork_link',]

class ProfilesSerializer(ProfileStatisticsMixin, serializers.ModelSerializer):
    profile_photo = serializers.ImageField(use_url = True)
    profile_photo_url = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()
    favorite_game = serializers.SerializerMethodField()
    favorite_game_id = serializers.IntegerField(write_only = True, required = False, allow_null = True)

    class Meta:
        model = Profiles
        fields = ['id', 'user', 'display_name', 'profile_photo', 'profile_photo_url', 'private_profile', 'website_theme', 'bio', 'favorite_game', 'favorite_game_id', 'favorite_developer', 'favorite_publisher', 'favorite_genre', 'favorite_platform', 'favorite_franchise', 'favorite_series', 'playstyle', 'statistics']
        read_only_fields = ['id', 'user']

    def get_profile_photo_url(self, obj):
        request = self.context.get('request')
        if obj.profile_photo and request:
            return request.build_absolute_uri(obj.profile_photo.url)
        return None

    def get_statistics(self, obj):
        return self.statistics(obj)
    
    def get_favorite_game(self, obj):
        if not obj.favorite_game:
            return None
        return {'id': obj.favorite_game.id, 'igdb_id': obj.favorite_game.igdb_id, 'game_title': obj.favorite_game.game_title, 'cover_artwork_link': obj.favorite_game.cover_artwork_link,}
    
    def update(self, instance, validated_data):
        favorite_game_id = validated_data.pop('favorite_game_id', object())
        if favorite_game_id is not object():
            if favorite_game_id:
                instance.favorite_game = Games.objects.get(igdb_id = favorite_game_id)
            else:
                instance.favorite_game = None
        instance.save()
        return super().update(instance, validated_data)

class UsersSerializer(ProfileStatisticsMixin, serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username')
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = Profiles
        fields = ['username', 'profile_photo', 'bio', 'statistics']

    def get_statistics(self, obj):
        return self.statistics(obj)

class APIKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKeys
        fields = ['id', 'user', 'api_token_prefix', 'creation_timestamp', 'last_fetched', 'rotate', 'expiration_date', 'expired']
        read_only_fields = ['id', 'user', 'api_token_prefix', 'creation_timestamp', 'last_fetched', 'rotate', 'expiration_date']