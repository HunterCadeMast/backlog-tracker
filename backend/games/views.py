from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from games.models import Games
from games.serializers import GamesSerializer
from games.services import request_game_info_by_name
from games.transfer import games_database_transfer

class GamePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

class GamesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GamesSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    pagination_class = GamePagination

    def get_queryset(self):
        queryset = Games.objects.all()
        search = self.request.query_params.get('search')
        if not search:
            return queryset
        filtered_games = queryset.filter(game_title__icontains = search)
        if filtered_games.exists() and len(search) >= 3:
            return filtered_games
        igdb_data = request_game_info_by_name(search)
        if not igdb_data:
            return queryset.none()
        for game_data in igdb_data:
            games_database_transfer(game_data)
        return Games.objects.filter(game_title__icontains = search)