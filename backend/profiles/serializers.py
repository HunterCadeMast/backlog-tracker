from rest_framework import serializers
from django.db.models import Sum
from collections import Counter, defaultdict
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
            yearly_games[year] += 1

        def top_favorites(objects_list, top_few = 3):
            if not objects_list:
                return []
            counts = Counter(objects_list)
            most_common = counts.most_common(top_few)
            if not most_common:
                return []
            max_count = most_common[0][1]
            tie_count = sum(1 for v in counts.values() if v == max_count)
            if tie_count > top_few:
                return []
            return [{'id': obj.id, 'label': getattr(obj, 'label', getattr(obj, 'name', ''))} for obj, _ in most_common]
        all_developers = []
        all_publishers = []
        all_genres = []
        all_platforms = []
        all_franchises = []
        all_series = []
        for log in logs:
            game = log.game_id
            if not game:
                continue
            all_developers.extend(related.developer_id for related in game.gamespecificdevelopers_set.all())
            all_publishers.extend(related.publisher_id for related in game.gamespecificpublishers_set.all())
            all_genres.extend(related.genre_id for related in game.gamespecificgenres_set.all())
            all_platforms.extend(related.platform_id for related in game.gamespecificplatforms_set.all())
            all_franchises.extend(related.franchise_id for related in game.gamespecificfranchises_set.all())
            all_series.extend(related.series_id for related in game.gamespecificseries_set.all())
        favorite_developers = top_favorites(all_developers)
        favorite_publishers = top_favorites(all_publishers)
        favorite_genres = top_favorites(all_genres)
        favorite_platforms = top_favorites(all_platforms)
        favorite_franchises = top_favorites(all_franchises)
        favorite_series = top_favorites(all_series)
        data = {
            'total_games': logs.count(),
            'completed_games': completed_games.count(),
            'playing_games': playing_games.count(),
            'backlog_games': backlog_games.count(),
            'dropped_games': dropped_games.count(),
            'paused_games': paused_games.count(),
            'total_playtime': logs.aggregate(total = Sum('user_playtime'))['total'] or 0,
            'yearly_completed_games': dict(yearly_games),
            'favorite_developers': favorite_developers,
            'favorite_publishers': favorite_publishers,
            'favorite_genres': favorite_genres,
            'favorite_platforms': favorite_platforms,
            'favorite_franchises': favorite_franchises,
            'favorite_series': favorite_series,
        }
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