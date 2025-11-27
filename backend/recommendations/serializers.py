from rest_framework import serializers
from recommendations.models import Recommendations

class RecommendationsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Recommendations
        fields = ['id', 'profile_id', 'game_id', 'user', 'recommendation_match', 'creation_timestamp']
        read_only_fields = ['id', 'profile_id', 'game_id', 'user', 'creation_timestamp']