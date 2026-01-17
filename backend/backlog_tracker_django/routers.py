from rest_framework import routers
from profiles.views import ProfilesViewSet, UsersViewSet, APIKeysViewSet
from games.views import GamesViewSet
from logs.views import LogsViewSet, LogSessionsViewSet, LogTagsViewSet
from playlists.views import PlaylistsViewSet, PlaylistLogsViewSet
from recommendations.views import RecommendationsViewSet

router = routers.SimpleRouter()

# Profiles Routing
router.register(r'profiles', ProfilesViewSet, basename = "profiles")
router.register(r'api_keys', APIKeysViewSet, basename = "api_keys")

# Logs Routing
router.register(r'games', GamesViewSet, basename='games')
router.register(r'logs', LogsViewSet, basename = "logs")
router.register(r'log_sessions', LogSessionsViewSet, basename = "log_sessions")
router.register(r'log_tags', LogTagsViewSet, basename = "log_tags")

# Playlists Routing
router.register(r'playlists', PlaylistsViewSet, basename = "playlists")
router.register(r'playlist_logs', PlaylistLogsViewSet, basename = "playlist_logs")

# Recommendations Routing
router.register(r'recommendations', RecommendationsViewSet, basename = "recommendations")

urlpatterns = router.urls