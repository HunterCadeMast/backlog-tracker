from django.db import models
from django.utils import timezone
from profiles.models import Profiles
from games.models import Games, Platforms
from accounts.models import CustomUser
import uuid

class Logs(models.Model):
    STATUS_TYPES = [('backlog', 'Backlog'), ('playing', 'Playing'), ('paused', 'Paused'), ('completed', 'Completed'), ('dropped', 'Dropped')]
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null = False, blank = False)
    profile_id = models.ForeignKey(Profiles, on_delete = models.CASCADE, null = False, blank = False)
    game_id = models.ForeignKey(Games, on_delete = models.CASCADE, null = False, blank = False)
    platform_id = models.ForeignKey(Platforms, on_delete = models.CASCADE, null = False, blank = False)
    user_status = models.CharField(max_length = 12, choices = STATUS_TYPES, default = 'backlog', null = False, blank = False)
    user_rating = models.IntegerField(null = True, blank = True)
    user_review = models.TextField(max_length = 255, null = True, blank = True)
    user_playtime = models.IntegerField(null = True, blank = True)
    start_date = models.DateField(null = True, blank = True)
    completion_date = models.DateField(null = True, blank = True)
    creation_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['profile_id', 'game_id', 'platform_id'], name = 'user_entry_logs')
        ]

    def __str__(self):
        return f"{self.user.username} logged {self.game_id.game_title} on {self.platform_id.label}"
    
class LogTags(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null = False, blank = False)
    profile_id = models.ForeignKey(Profiles, on_delete = models.CASCADE, null = False, blank = False)
    log_id = models.ForeignKey(Logs, on_delete = models.CASCADE, null = False, blank = False)
    log_tag = models.CharField(max_length = 32, null = False, blank = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['log_id', 'log_tag'], name = 'log_entry_tags')
        ]

    def __str__(self):
        return f"{self.log_id.game_id.game_title} is tagged as {self.log_tag}"