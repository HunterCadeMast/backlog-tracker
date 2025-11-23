from django.db import models
from django.utils import timezone
import uuid

class Profiles(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    username = models.CharField(max_length = 35, unique = True, null = True, blank = True)
    email = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    hashed_password = models.TextField(null = True, blank = True)
    creation_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)

    def __str__(self):
        return self.username
    
class OAuthenticationTokens(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    profile_id = models.ForeignKey(Profiles, on_delete = models.CASCADE, null = False, blank = False)
    provider_id = models.CharField(max_length = 12, null = False, blank = False)
    provider_name = models.CharField(max_length = 255, null = False, blank = False)
    access_token = models.TextField(null = True, blank = True)
    refresh_token = models.TextField(null = True, blank = True)
    creation_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)
    expiration_date = models.DateTimeField(null = True, blank = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['provider_id', 'provider_name'], name = 'Provider for User\'s OAuthentication')
        ]

    def __str__(self):
        return f"OAuthentication for {self.profile_id.username}"
    
class APIKeys(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    profile_id = models.ForeignKey(Profiles, on_delete = models.CASCADE, null = False, blank = False)
    api_token = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    creation_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)
    last_fetched = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return f"{self.profile_id.username}\'s API Keys"
    
class SteamProfiles(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    steam_id = models.CharField(max_length = 18, null = True, blank = True)
    steam_username = models.CharField(max_length = 32, null = True, blank = True)
    steam_avatar_link = models.TextField(null = True, blank = True)
    creation_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)
    last_fetched = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return self.steam_username