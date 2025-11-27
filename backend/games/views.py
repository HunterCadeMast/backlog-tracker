from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from games.models import Games, Developers, GameSpecificDevelopers, Publishers, GameSpecificPublishers, Genres, GameSpecificGenres, Platforms, GameSpecificPlatforms, Franchises, GameSpecificFranchises, Series, GameSpecificSeries
from games.serializers import GamesSerialiser, DevelopersSerialiser, GameSpecificDevelopersSerialiser, PublishersSerialiser, GameSpecificPublishersSerialiser, GenresSerialiser, GameSpecificGenresSerialiser, PlatformsSerialiser, GameSpecificPlatformsSerialiser, FranchisesSerialiser, GameSpecificFranchisesSerialiser, SeriesSerialiser, GameSpecificSeriesSerialiser

class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class DevelopersViewSet(viewsets.ModelViewSet):
    queryset = Developers.objects.all()
    serializer_class = DevelopersSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class GameSpecificDevelopersViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificDevelopers.objects.all()
    serializer_class = GameSpecificDevelopersSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class PublishersViewSet(viewsets.ModelViewSet):
    queryset = Publishers.objects.all()
    serializer_class = PublishersSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class GameSpecificPublishersViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificPublishers.objects.all()
    serializer_class = GameSpecificPublishersSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class GameSpecificGenresViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificGenres.objects.all()
    serializer_class = GameSpecificGenresSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class PlatformsViewSet(viewsets.ModelViewSet):
    queryset = Platforms.objects.all()
    serializer_class = PlatformsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class GameSpecificPlatformsViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificPlatforms.objects.all()
    serializer_class = GameSpecificPlatformsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class FranchisesViewSet(viewsets.ModelViewSet):
    queryset = Franchises.objects.all()
    serializer_class = FranchisesSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class GameSpecificFranchisesViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificFranchises.objects.all()
    serializer_class = GameSpecificFranchisesSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class GameSpecificSeriesViewSet(viewsets.ModelViewSet):
    queryset = GameSpecificSeries.objects.all()
    serializer_class = GameSpecificSeriesSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]