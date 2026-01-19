from rest_framework import serializers
from django.utils import timezone
from logs.models import Logs, LogSessions, LogTags
from games.serializers import GamesSerializer

class LogsSerializer(serializers.ModelSerializer):
    game = GamesSerializer(source = 'game_id', read_only = True)

    class Meta:
        model = Logs
        fields = ['id', 'user', 'profile_id', 'game_id', 'platform_id', 'game', 'user_status', 'user_rating', 'user_review', 'user_playtime', 'start_date', 'completion_date', 'full_completion', 'creation_timestamp',]
        read_only_fields = ['id', 'creation_timestamp']

    def validate(self, data):
        start = data.get("start_date")
        end = data.get("completion_date")
        today = timezone.now().date()
        if start and start > today:
            raise serializers.ValidationError("Start date cannot be in the future!")
        if end and end > today:
            raise serializers.ValidationError("Completion date cannot be in the future!")
        if start and end and end < start:
            raise serializers.ValidationError("Completion date cannot be before the start date!")
        return data

class LogSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSessions
        fields = ['id', 'log_id', 'session_playtime', 'start_time', 'end_time', 'creation_timestamp']
        read_only_fields = ['id', 'log_id', 'session_playtime', 'creation_timestamp']

class LogTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogTags
        fields = ['id', 'user', 'profile_id', 'log_id', 'log_tag']
        read_only_fields = ['id', 'user', 'profile_id', 'log_id']