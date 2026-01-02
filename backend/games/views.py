from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from games.models import Games
from games.serializers import GamesSerializer
from games.services import request_game_info_by_name
import requests

class GamePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 1000

class GamesViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    pagination_class = GamePagination

    def list(self, request):
        search = request.query_params.get("search", "").strip()
        queryset = Games.objects.all()
        if not search:
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = GamesSerializer(page, many = True)
            return paginator.get_paginated_response(serializer.data)
        try:
            igdb_titles = request_game_info_by_name(search)
        except requests.HTTPError:
            igdb_titles = []
        local_titles = {game.game_title for game in queryset}
        total_titles = []
        for game in igdb_titles:
            if game["name"] in local_titles:
                title = queryset.get(game_title = game["name"])
                total_titles.append(title)
            else:
                total_titles.append(Games(id = game.get("id") or 0, game_title = game["name"], cover_artwork_link = game.get("cover", {}).get("url"),))
        if len(search) >= 3:
            local_search = queryset.filter(game_title__icontains = search)
            for game in local_search:
                if game not in total_titles:
                    total_titles.append(g)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(total_titles, request)
        serializer = GamesSerializer(page, many = True)
        return paginator.get_paginated_response(serializer.data)
