from django.db import models
from django.utils import timezone
from profiles.models import Profiles
from games.models import Games
import uuid

class Recommendations(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    profile_id = models.ForeignKey(Profiles, on_delete = models.CASCADE, null = False, blank = False)
    game_id = models.ForeignKey(Games, on_delete = models.CASCADE, null = False, blank = False)
    recommendation_match = models.DecimalField(max_digits = 4, decimal_places = 2, null = False, blank = False)
    creation_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)

    def __str__(self):
        return f"{self.profile_id.username} recommendations include {self.game_id.game_title}"