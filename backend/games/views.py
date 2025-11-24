from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from games.models import Games, Developers, GameSpecificDevelopers, Publishers, GameSpecificPublishers, Genres, GameSpecificGenres, Platforms, GameSpecificPlatforms, Franchises, GameSpecificFranchises, Series, GameSpecificSeries
from games.serializers import GamesSerialiser, DevelopersSerialiser, GameSpecificDevelopersSerialiser, PublishersSerialiser, GameSpecificPublishersSerialiser, GenresSerialiser, GameSpecificGenresSerialiser, PlatformsSerialiser, GameSpecificPlatformsSerialiser, FranchisesSerialiser, GameSpecificFranchisesSerialiser, SeriesSerialiser, GameSpecificSeriesSerialiser

class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerialiser
    permission_classes = [AllowAny]

class DevelopersViewSet(viewsets.ModelViewSet):
    queryset = Developers.objects.all()
    serializer_class = DevelopersSerialiser
    permission_classes = [AllowAny]

class GameSpecificDevelopersViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificDevelopers.objects.all()
    serializer_class = GameSpecificDevelopersSerialiser
    permission_classes = [AllowAny]

class PublishersViewSet(viewsets.ModelViewSet):
    queryset = Publishers.objects.all()
    serializer_class = PublishersSerialiser
    permission_classes = [AllowAny]

class GameSpecificPublishersViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificPublishers.objects.all()
    serializer_class = GameSpecificPublishersSerialiser
    permission_classes = [AllowAny]

class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerialiser
    permission_classes = [AllowAny]

class GameSpecificGenresViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificGenres.objects.all()
    serializer_class = GameSpecificGenresSerialiser
    permission_classes = [AllowAny]

class PlatformsViewSet(viewsets.ModelViewSet):
    queryset = Platforms.objects.all()
    serializer_class = PlatformsSerialiser
    permission_classes = [AllowAny]

class GameSpecificPlatformsViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificPlatforms.objects.all()
    serializer_class = GameSpecificPlatformsSerialiser
    permission_classes = [AllowAny]

class FranchisesViewSet(viewsets.ModelViewSet):
    queryset = Franchises.objects.all()
    serializer_class = FranchisesSerialiser
    permission_classes = [AllowAny]

class GameSpecificFranchisesViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificFranchises.objects.all()
    serializer_class = GameSpecificFranchisesSerialiser
    permission_classes = [AllowAny]

class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerialiser
    permission_classes = [AllowAny]

class GameSpecificSeriesViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificSeries.objects.all()
    serializer_class = GameSpecificSeriesSerialiser
    permission_classes = [AllowAny]