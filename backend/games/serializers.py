from rest_framework import serializers
from games.models import Games, Developers, GameSpecificDevelopers, Publishers, GameSpecificPublishers, Genres, GameSpecificGenres, Platforms, GameSpecificPlatforms, Franchises, GameSpecificFranchises, Series, GameSpecificSeries

class GamesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'igdb_id', 'game_title', 'cover_artwork_link', 'release_date', 'completion_time', 'completionist_completion_time', 'average_rating']
        read_only_fields = ['id', 'igdb_id', 'game_title', 'cover_artwork_link', 'release_date', 'completion_time', 'completionist_completion_time', 'average_rating']

class DevelopersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Developers
        fields = ['id', 'label']
        read_only_fields = ['id', 'label']

class GameSpecificDevelopersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = GameSpecificDevelopers
        fields = ['id', 'game_id', 'developer_id']
        read_only_fields = ['id', 'game_id', 'developer_id']

class PublishersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Publishers
        fields = ['id', 'label']
        read_only_fields = ['id', 'label']

class GameSpecificPublishersSerialiser(serializers.ModelSerializer):
    class Meta:
        model = GameSpecificPublishers
        fields = ['id', 'game_id', 'publisher_id']
        read_only_fields = ['id', 'game_id', 'publisher_id']

class GenresSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ['id', 'label']
        read_only_fields = ['id', 'label']

class GameSpecificGenresSerialiser(serializers.ModelSerializer):
    class Meta:
        model = GameSpecificGenres
        fields = ['id', 'game_id', 'genre_id']
        read_only_fields = ['id', 'game_id', 'genre_id']

class PlatformsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Platforms
        fields = ['id', 'label']
        read_only_fields = ['id', 'label']

class GameSpecificPlatformsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = GameSpecificPlatforms
        fields = ['id', 'game_id', 'platform_id']
        read_only_fields = ['id', 'game_id', 'platform_id']

class FranchisesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Franchises
        fields = ['id', 'label']
        read_only_fields = ['id', 'label']

class GameSpecificFranchisesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = GameSpecificFranchises
        fields = ['id', 'game_id', 'franchise_id']
        read_only_fields = ['id', 'game_id', 'franchise_id']

class SeriesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['id', 'label']
        read_only_fields = ['id', 'label']

class GameSpecificSeriesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = GameSpecificSeries
        fields = ['id', 'game_id', 'series_id']
        read_only_fields = ['id', 'game_id', 'series_id']