from django.db import models
from django.utils import timezone
from profiles.models import Profiles
from logs.models import Logs
from accounts.models import CustomUser
import uuid

class Playlists(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null = False, blank = False)
    profile_id = models.ForeignKey(Profiles, on_delete = models.CASCADE, null = False, blank = False)
    playlist_title = models.CharField(max_length = 32, null = False, blank = False)
    creation_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)
    updated_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['profile_id', 'playlist_title'], name = 'user_playlists')
        ]

    def update_time(self):
        self.updated_timestamp = timezone.now()
        self.save(update_fields = ['updated_timestamp'])

    def __str__(self):
        return f"{self.profile_id.username} created a playlist called {self.playlist_title}"
    
class PlaylistLogs(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null = False, blank = False)
    playlist_id = models.ForeignKey(Playlists, on_delete = models.CASCADE, null = False, blank = False)
    log_id = models.ForeignKey(Logs, on_delete = models.CASCADE, null = False, blank = False)
    current_position = models.IntegerField(null = True, blank = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['playlist_id', 'log_id'], name = 'user_playlist_entry_logs')
        ]

    def __str__(self):
        return f"{self.log_id.game_id.game_title} is in the playlist called {self.playlist_id.playlist_title}"