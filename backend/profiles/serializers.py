from rest_framework import serializers
from django.db.models import Sum
from collections import Counter, defaultdict
from accounts.models import CustomUser
from profiles.models import Profiles, APIKeys
from games.models import Games
from logs.models import Logs
from logs.serializers import LogsSerializer

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
        
        def calculate_playstyle_scores(logs):
            scores = defaultdict(int)
            for log in logs:
                game = log.game_id
                playtime = log.user_playtime or 0
                if playtime < 10:
                    scores['casual'] += 1
                if log.user_status == 'completed':
                    scores['completionist'] += 2
                if playtime > 30:
                    scores['completionist'] += 1
                scores['heavy_gamer'] += playtime / 50
                if game:
                    genres = game.gamespecificgenres_set.all()
                    for genre in genres:
                        label = genre.genre_id.label.lower()
                        if label in ['rpg', 'adventure']:
                            scores['story_focused'] += 2
                        if label in ['action', 'platformer', 'roguelike']:
                            scores['gameplay_focused'] += 2
                        if label == 'indie':
                            scores['indie_gamer'] += 2
            multiplayer_count = logs.filter(is_multiplayer = True).count() if hasattr(Logs, 'is_multiplayer') else 0
            scores['multiplayer'] += multiplayer_count * 2
            scores['single_player'] += (logs.count() - multiplayer_count)
            primary = max(scores, key = scores.get) if scores else 'casual'
            return {'primary': primary, 'scores': dict(scores)}
        
        def commitment_chart(logs):
            commitments = {'0 - 5 Hours': 0, '5 - 10 Hours': 0, '10 - 30 Hours': 0, '30 - 60 Hours': 0, '60 - 100 Hours': 0, '100+ Hours': 0,}
            played_logs = logs.exclude(user_status = 'backlog')
            for log in played_logs:
                Hours = log.user_playtime or 0
                if Hours <= 5:
                    commitments['0 - 5 Hours'] += 1
                elif Hours <= 10:
                    commitments['5 - 10 Hours'] += 1
                elif Hours <= 30:
                    commitments['10 - 30 Hours'] += 1
                elif Hours <= 60:
                    commitments['30 - 60 Hours'] += 1
                elif Hours <= 100:
                    commitments['60 - 100 Hours'] += 1
                else:
                    commitments['100+ Hours'] += 1
            return commitments
        
        def genre_variety(logs):
            genres = []
            for log in logs:
                if log.game_id:
                    genres.extend(genre.genre_id.label for genre in log.game_id.gamespecificgenres_set.all())
            unique_genres = len(set(genres))
            total_games = logs.count()
            return {'unique_genres': unique_genres, 'total_games': total_games, 'index': unique_genres / max(total_games, 1)}
        
        def dropoff_depth(logs):
            dropped = logs.filter(user_status = 'dropped')
            avg = dropped.aggregate(avg = Sum('user_playtime'))['avg'] or 0
            return avg / max(dropped.count(), 1)

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
        playstyle_data = calculate_playstyle_scores(logs)
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
            'playstyle': playstyle_data,
            'commitment_chart': commitment_chart(logs),
            'genre_variety': genre_variety(logs),
            'dropoff_depth': dropoff_depth(logs),
        }
        return data
    
class FavoriteGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'igdb_id', 'game_title', 'cover_artwork_link',]

class ProfilesSerializer(ProfileStatisticsMixin, serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username')
    has_password = serializers.SerializerMethodField()
    providers = serializers.SerializerMethodField()
    profile_photo = serializers.ImageField(use_url = True)
    profile_photo_url = serializers.SerializerMethodField()
    logs = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()
    favorite_game = serializers.SerializerMethodField()
    favorite_game_id = serializers.IntegerField(write_only = True, required = False, allow_null = True)

    class Meta:
        model = Profiles
        fields = ['id', 'user', 'username', 'has_password', 'providers', 'profile_photo', 'profile_photo_url', 'private_profile', 'website_theme', 'bio', 'logs', 'favorite_game', 'favorite_game_id', 'favorite_developer', 'favorite_publisher', 'favorite_genre', 'favorite_platform', 'favorite_franchise', 'favorite_series', 'playstyle', 'statistics']
        read_only_fields = ['id', 'user']

    def get_has_password(self, obj):
        return obj.user.has_usable_password()

    def get_providers(self, obj):
        return list(obj.user.socialaccount_set.values_list('provider', flat = True))
    
    def get_profile_photo_url(self, obj):
        request = self.context.get('request')
        if obj.profile_photo and request:
            return request.build_absolute_uri(obj.profile_photo.url)
        return None
    
    def get_logs(self, obj):
        return LogsSerializer(Logs.objects.filter(user = obj.user), many = True).data

    def get_statistics(self, obj):
        return self.statistics(obj)
    
    def get_favorite_game(self, obj):
        if not obj.favorite_game:
            return None
        return {'id': obj.favorite_game.id, 'igdb_id': obj.favorite_game.igdb_id, 'game_title': obj.favorite_game.game_title, 'cover_artwork_link': obj.favorite_game.cover_artwork_link,}

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data and 'username' in user_data:
            new_username = user_data['username']
            if (CustomUser.objects.exclude(id = instance.user.id).filter(username = new_username).exists()):
                raise serializers.ValidationError({'username': 'This username is already taken!'})
            instance.user.username = new_username
            instance.user.save()
        favorite_game_id = validated_data.pop('favorite_game_id', None)
        if favorite_game_id is None:
            instance.favorite_game = None
        elif isinstance(favorite_game_id, int):
            instance.favorite_game = Games.objects.get(igdb_id = favorite_game_id)
        else:
            raise serializers.ValidationError({'favorite_game_id': 'Must be an integer or null!'})
        instance.user.save()
        return super().update(instance, validated_data)

class UsersSerializer(ProfileStatisticsMixin, serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username')
    logs = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()
    favorite_game = serializers.SerializerMethodField()
    favorite_game_id = serializers.IntegerField(write_only = True, required = False, allow_null = True)

    class Meta:
        model = Profiles
        fields = ['username', 'profile_photo', 'bio', 'statistics', 'logs', 'favorite_game', 'favorite_game_id']
    
    def get_logs(self, obj):
        return LogsSerializer(Logs.objects.filter(user = obj.user), many = True).data

    def get_statistics(self, obj):
        return self.statistics(obj)
    
    def get_favorite_game(self, obj):
        if not obj.favorite_game:
            return None
        return {'id': obj.favorite_game.id, 'igdb_id': obj.favorite_game.igdb_id, 'game_title': obj.favorite_game.game_title, 'cover_artwork_link': obj.favorite_game.cover_artwork_link,}

class APIKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKeys
        fields = ['id', 'user', 'api_token_prefix', 'creation_timestamp', 'last_fetched', 'rotate', 'expiration_date', 'expired']
        read_only_fields = ['id', 'user', 'api_token_prefix', 'creation_timestamp', 'last_fetched', 'rotate', 'expiration_date']