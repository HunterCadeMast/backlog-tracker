from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from games.models import Games
from games.serializers import GamesSerializer
from games.services import request_game_info_by_name, fetch_game_info
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
        seen = set()
        total_titles = []
        for game in igdb_titles:
            igdb_id = game.get("id")
            if not igdb_id or igdb_id in seen:
                continue
            seen.add(igdb_id)
            local_title = Games.objects.filter(igdb_id = igdb_id).first()
            if local_title:
                total_titles.append(local_title)
            else:
                total_titles.append(Games(igdb_id = game["id"], game_title = game["name"], cover_artwork_link = game.get("cover", {}).get("url"),))
        if len(search) >= 3:
            for game in queryset:
                if search.lower() in game.game_title.lower() and (game.igdb_id not in seen):
                    total_titles.append(game)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(total_titles, request)
        serializer = GamesSerializer(page, many = True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail = False, methods = ['get'], url_path = r"(?P<igdb_id>\d+)")
    def fetch(self, request, igdb_id = None):
        game = Games.objects.filter(igdb_id = igdb_id).first()
        if not game:
            igdb_data = fetch_game_info(int(igdb_id))
            if not igdb_data:
                return Response({'error': 'Game not found!'}, status = 404)
            cover_url = None
            if igdb_data.get('cover'):
                cover_url = igdb_data["cover"]["url"].replace("t_thumb", "t_cover_big")
            rating = None
            if igdb_data.get('rating'):
                rating = int(igdb_data['rating'])
            game = Games.objects.create(igdb_id = igdb_data['id'], game_title = igdb_data['name'], cover_artwork_link = cover_url, average_rating = rating)
        return Response(GamesSerializer(game).data)
