from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from games.models import Games, Developers, Publishers, Genres, Platforms, Franchises, Series
from PIL import Image
import uuid

class Profiles(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    display_name = models.CharField(max_length = 32, null = True, blank = True)
    profile_photo = models.ImageField(default = 'profile_pictures/default.jpg', upload_to = 'profile_pictures')
    private_profile = models.BooleanField(default = False, null = False, blank = False)
    THEME_TYPES = [('dark', 'Dark'), ('light', 'Light'), ('orange', 'Orange'), ('lemon', 'Lemon'), ('strawberry', 'Strawberry'), ('blueberry', 'Blueberry')]
    website_theme = models.CharField(max_length = 20, choices = THEME_TYPES, default = 'dark', null = False, blank = False)
    bio = models.TextField(max_length = 255, null = True, blank = True)
    favorite_game = models.ManyToManyField(Games, null = False, blank = True)
    favorite_developer = models.ManyToManyField(Developers, null = False, blank = True)
    favorite_publisher = models.ManyToManyField(Publishers, null = False, blank = True)
    favorite_genre = models.ManyToManyField(Genres, null = False, blank = True)
    favorite_platform = models.ManyToManyField(Platforms, null = False, blank = True)
    favorite_franchise = models.ManyToManyField(Franchises, null = False, blank = True)
    favorite_series = models.ManyToManyField(Series, null = False, blank = True)
    PLAYSTYLE_TYPES = [('casual', 'Casual'), ('completionist', 'Completionist'), ('story_focused', 'Story Focused'), ('gameplay_focused', 'Gameplay Focused'), ('indie_gamer', 'Indie Gamer'), ('heavy_gamer', 'Heavy Gamer'), ('competitive_gamer', 'Competitive Gamer'), ('single_player', 'Single-Player'), ('multi_player', 'Multi-Player')]
    playstyle = models.CharField(max_length = 32, choices = PLAYSTYLE_TYPES, default = 'casual', null = True, blank = True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile_photo = Image.open(self.image.path)
        if profile_photo.height > 300 or profile_photo.width > 300:
            profile_photo.thumbnail((300, 300))
            profile_photo.save()
    
class APIKeys(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null = False, blank = False)
    api_token_prefix = models.CharField(max_length = 8, unique = True, null = False, blank = False)
    creation_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)
    last_fetched = models.DateTimeField(null = True, blank = True)
    rotate = models.ForeignKey('self', on_delete = models.SET_NULL, null = True, blank = True)
    expiration_date = models.DateTimeField(null = True, blank = True)
    expired = models.BooleanField(default = False, null = False, blank = False)

    def __str__(self):
        return f"{self.profile_id.username}\'s API Keys"