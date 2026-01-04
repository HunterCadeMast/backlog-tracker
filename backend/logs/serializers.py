from rest_framework import serializers
from logs.models import Logs, LogSessions, LogTags
from games.serializers import GamesSerializer

class LogsSerializer(serializers.ModelSerializer):
    game = GamesSerializer(source = 'game_id', read_only = True)

    class Meta:
        model = Logs
        fields = ['id', 'user', 'profile_id', 'game_id', 'platform_id', 'game', 'user_status', 'user_rating', 'user_review', 'user_playtime', 'start_date', 'completion_date', 'full_completion', 'creation_timestamp',]
        read_only_fields = ['id', 'creation_timestamp']

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