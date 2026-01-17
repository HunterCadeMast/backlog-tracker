from django.db import models
import uuid

class Games(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    igdb_id = models.IntegerField(unique = True, null = True, blank = True)
    game_title = models.CharField(max_length = 255, null = False, blank = False)
    cover_artwork_link = models.TextField(null = True, blank = True)
    summary = models.TextField(null = True, blank = True)
    release_date = models.DateField(null = True, blank = True)
    completion_time = models.IntegerField(null = True, blank = True)
    completionist_completion_time = models.IntegerField(null = True, blank = True)
    average_rating = models.IntegerField(null = True, blank = True)

    def __str__(self):
        return self.game_title
    
class Developers(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    label = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    
    def __str__(self):
        return self.label

class GameSpecificDevelopers(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    game_id = models.ForeignKey(Games, on_delete = models.CASCADE, null = False, blank = False)
    developer_id = models.ForeignKey(Developers, on_delete = models.CASCADE, null = False, blank = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['game_id', 'developer_id'], name = 'Developers for a Specific Game')
        ]

    def __str__(self):
        return f"{self.game_id.game_title} developed by {self.developer_id.label}"

class Publishers(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    label = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    
    def __str__(self):
        return self.label

class GameSpecificPublishers(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    game_id = models.ForeignKey(Games, on_delete = models.CASCADE, null = False, blank = False)
    publisher_id = models.ForeignKey(Publishers, on_delete = models.CASCADE, null = False, blank = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['game_id', 'publisher_id'], name = 'Publishers for a Specific Game')
        ]

    def __str__(self):
        return f"{self.game_id.game_title} published by {self.publisher_id.label}"
    
class Genres(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    label = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    
    def __str__(self):
        return self.label

class GameSpecificGenres(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    game_id = models.ForeignKey(Games, on_delete = models.CASCADE, null = False, blank = False)
    genre_id = models.ForeignKey(Genres, on_delete = models.CASCADE, null = False, blank = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['game_id', 'genre_id'], name = 'Genres for a Specific Game')
        ]

    def __str__(self):
        return f"{self.game_id.game_title} in the genres of {self.genre_id.label}"
    
class Platforms(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    label = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    
    def __str__(self):
        return self.label

class GameSpecificPlatforms(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    game_id = models.ForeignKey(Games, on_delete = models.CASCADE, null = False, blank = False)
    platform_id = models.ForeignKey(Platforms, on_delete = models.CASCADE, null = False, blank = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['game_id', 'platform_id'], name = 'Platforms for a Specific Game')
        ]

    def __str__(self):
        return f"{self.game_id.game_title} on the platforms of {self.platform_id.label}"
    
class Franchises(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    label = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    
    def __str__(self):
        return self.label

class GameSpecificFranchises(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    game_id = models.ForeignKey(Games, on_delete = models.CASCADE, null = False, blank = False)
    franchise_id = models.ForeignKey(Franchises, on_delete = models.CASCADE, null = False, blank = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['game_id', 'franchise_id'], name = 'Franchises for a Specific Game')
        ]

    def __str__(self):
        return f"{self.game_id.game_title} in the franchises of {self.franchise_id.label}"
    
class Series(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    label = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    
    def __str__(self):
        return self.label

class GameSpecificSeries(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    game_id = models.ForeignKey(Games, on_delete = models.CASCADE, null = False, blank = False)
    series_id = models.ForeignKey(Series, on_delete = models.CASCADE, null = False, blank = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['game_id', 'series_id'], name = 'Series for a Specific Game')
        ]

    def __str__(self):
        return f"{self.game_id.game_title} in the series of {self.series_id.label}"