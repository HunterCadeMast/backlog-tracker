from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
import uuid

class SteamProfiles(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    steam_id = models.CharField(max_length = 18, unique = True, null = True, blank = True)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null = False, blank = False)
    steam_username = models.CharField(max_length = 32, null = True, blank = True)
    steam_avatar_link = models.TextField(null = True, blank = True)
    steam_public_profile = models.BooleanField(default = True, null = True, blank = True)
    auto_sync_playtime = models.BooleanField(default = False, null = True, blank = True)
    auto_sync_games = models.BooleanField(default = False, null = True, blank = True)
    creation_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)
    last_fetched = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return self.steam_username