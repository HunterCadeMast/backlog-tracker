from rest_framework import routers
from profiles.views import ProfilesViewSet, APIKeysViewSet
from games.views import GamesViewSet, DevelopersViewSet, GameSpecificDevelopersViewSet, PublishersViewSet, GameSpecificPublishersViewSet, GenresViewSet, GameSpecificGenresViewSet, PlatformsViewSet, GameSpecificPlatformsViewSet, FranchisesViewSet, GameSpecificFranchisesViewSet, SeriesViewSet, GameSpecificSeriesViewSet
from logs.views import LogsViewSet, LogTagsViewSet
from playlists.views import PlaylistsViewSet, PlaylistLogsViewSet
from recommendations.views import RecommendationsViewSet

router = routers.SimpleRouter()

# Profiles Routing
router.register(r'profile', ProfilesViewSet, basename = "profile")
router.register(r'api_keys', APIKeysViewSet, basename = "api_keys")

# Games Routing
router.register(r'games', GamesViewSet, basename = "games")
router.register(r'developers', DevelopersViewSet, basename = "developers")
router.register(r'game_specific_developers', GameSpecificDevelopersViewSet, basename = "game_specific_developers")
router.register(r'publishers', PublishersViewSet, basename = "publishers")
router.register(r'game_specific_publishers', GameSpecificPublishersViewSet, basename = "game_specific_publishers")
router.register(r'genres', GenresViewSet, basename = "genres")
router.register(r'game_specific_genres', GameSpecificGenresViewSet, basename = "game_specific_genres")
router.register(r'platforms', PlatformsViewSet, basename = "platforms")
router.register(r'game_specific_platforms', GameSpecificPlatformsViewSet, basename = "game_specific_platforms")
router.register(r'franchises', FranchisesViewSet, basename = "franchises")
router.register(r'game_specific_franchises', GameSpecificFranchisesViewSet, basename = "game_specific_franchises")
router.register(r'series', SeriesViewSet, basename = "series")
router.register(r'game_specific_series', GameSpecificSeriesViewSet, basename = "game_specific_series")

# Logs Routing
router.register(r'logs', LogsViewSet, basename = "logs")
router.register(r'log_tags', LogTagsViewSet, basename = "log_tags")

# Playlists Routing
router.register(r'playlists', PlaylistsViewSet, basename = "playlists")
router.register(r'playlist_logs', PlaylistLogsViewSet, basename = "playlist_logs")

# Recommendations Routing
router.register(r'recommendations', RecommendationsViewSet, basename = "recommendations")

urlpatterns = router.urls