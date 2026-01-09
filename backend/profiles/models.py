from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
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
    bio = models.TextField(default = '', max_length = 255, null = True, blank = True)
    favorite_game = models.ManyToManyField('games.Games', blank = True)
    favorite_developer = models.ManyToManyField('games.Developers', blank = True)
    favorite_publisher = models.ManyToManyField('games.Publishers', blank = True)
    favorite_genre = models.ManyToManyField('games.Genres', blank = True)
    favorite_platform = models.ManyToManyField('games.Platforms', blank = True)
    favorite_franchise = models.ManyToManyField('games.Franchises', blank = True)
    favorite_series = models.ManyToManyField('games.Series', blank = True)
    PLAYSTYLE_TYPES = [('casual', 'Casual'), ('completionist', 'Completionist'), ('story_focused', 'Story Focused'), ('gameplay_focused', 'Gameplay Focused'), ('indie_gamer', 'Indie Gamer'), ('heavy_gamer', 'Heavy Gamer'), ('competitive_gamer', 'Competitive Gamer'), ('single_player', 'Single-Player'), ('multi_player', 'Multi-Player')]
    playstyle = models.CharField(max_length = 32, choices = PLAYSTYLE_TYPES, default = 'casual', null = True, blank = True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.display_name and self.user:
            self.display_name = self.user.username
        super().save(*args, **kwargs)
        if self.profile_photo:
            image = Image.open(self.profile_photo.path)
            if image.height > 300 or image.width > 300:
                image.thumbnail((300, 300))
                image.save(self.profile_photo.path)
    
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