from rest_framework import serializers
from logs.models import Logs, LogTags

class LogsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = ['id', 'profile_id', 'game_id', 'platform_id', 'user', 'user_status', 'user_rating', 'user_playtime', 'start_date', 'completion_date', 'creation_timestamp',]
        read_only_fields = ['id', 'game_id', 'platform_id', 'user', 'creation_timestamp']

class LogTagsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = LogTags
        fields = ['id', 'log_id', 'log_tag', 'user']
        read_only_fields = ['id', 'log_id', 'user']