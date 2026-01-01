from rest_framework import serializers
from games.models import Games

class GamesSerializer(serializers.ModelSerializer):
    developers = serializers.SerializerMethodField()
    publishers = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    platforms = serializers.SerializerMethodField()
    franchises = serializers.SerializerMethodField()
    series = serializers.SerializerMethodField()

    class Meta:
        model = Games
        fields = '__all__'

    def get_developers(self, obj):
        return [x.developer_id.label for x in obj.gamespecificdevelopers_set.all()]
    
    def get_publishers(self, obj):
        return [x.publisher_id.label for x in obj.gamespecificpublishers_set.all()]
    
    def get_genres(self, obj):
        return [x.genre_id.label for x in obj.gamespecificgenres_set.all()]
    
    def get_platforms(self, obj):
        return [x.platform_id.label for x in obj.gamespecificplatforms_set.all()]
    
    def get_franchises(self, obj):
        return [x.franchise_id.label for x in obj.gamespecificfranchises_set.all()]
    
    def get_series(self, obj):
        return [x.series_id.label for x in obj.gamespecificseries_set.all()]