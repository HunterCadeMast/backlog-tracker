from rest_framework import serializers
from logs.models import Logs, LogTags

class LogsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = ['id', 'user', 'profile_id', 'game_id', 'platform_id', 'user_status', 'user_rating', 'user_review', 'user_playtime', 'start_date', 'completion_date', 'full_completion', 'creation_timestamp',]
        read_only_fields = ['id', 'user', 'profile_id', 'game_id', 'platform_id', 'creation_timestamp']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['user'] = self.context['request'].user.profiles
        return super().create(validated_data)

class LogTagsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = LogTags
        fields = ['id', 'user', 'profile_id', 'log_id', 'log_tag']
        read_only_fields = ['id', 'user', 'profile_id', 'log_id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['user'] = self.context['request'].user.profiles
        return super().create(validated_data)