from rest_framework import routers
from profiles.views import ProfilesViewSet, APIKeysViewSet
from games.views import GamesViewSet, DevelopersViewSet, GameSpecificDevelopersViewSet, PublishersViewSet, GameSpecificPublishersViewSet, GenresViewSet, GameSpecificGenresViewSet, PlatformsViewSet, GameSpecificPlatformsViewSet, FranchisesViewSet, GameSpecificFranchisesViewSet, SeriesViewSet, GameSpecificSeriesViewSet
from logs.views import LogsViewSet, LogTagsViewSet
from playlists.views import PlaylistsViewSet, PlaylistLogsViewSet
from recommendations.views import RecommendationsViewSet
from steam.views import SteamProfilesViewSet

router = routers.SimpleRouter()

# Profiles Routing
router.register(r'profile', ProfilesViewSet, basename = "profile")
router.register(r'api-keys', APIKeysViewSet, basename = "api-keys")

# Games Routing
router.register(r'games', GamesViewSet, basename = "games")
router.register(r'developers', DevelopersViewSet, basename = "developers")
router.register(r'game-specific-developers', GameSpecificDevelopersViewSet, basename = "game-specific-developers")
router.register(r'publishers', PublishersViewSet, basename = "publishers")
router.register(r'game-specific-publishers', GameSpecificPublishersViewSet, basename = "game-specific-publishers")
router.register(r'genres', GenresViewSet, basename = "genres")
router.register(r'game-specific-genres', GameSpecificGenresViewSet, basename = "game-specific-genres")
router.register(r'platforms', PlatformsViewSet, basename = "platforms")
router.register(r'game-specific-platforms', GameSpecificPlatformsViewSet, basename = "game-specific-platforms")
router.register(r'franchises', FranchisesViewSet, basename = "franchises")
router.register(r'game-specific-franchises', GameSpecificFranchisesViewSet, basename = "game-specific-franchises")
router.register(r'series', SeriesViewSet, basename = "series")
router.register(r'game-specific-series', GameSpecificSeriesViewSet, basename = "game-specific-series")

# Logs Routing
router.register(r'logs', LogsViewSet, basename = "logs")
router.register(r'log-tags', LogTagsViewSet, basename = "log-tags")

# Playlists Routing
router.register(r'playlists', PlaylistsViewSet, basename = "playlists")
router.register(r'palylist-logs', PlaylistLogsViewSet, basename = "playlist-logs")

# Recommendations Routing
router.register(r'recommendations', RecommendationsViewSet, basename = "recommendations")

# Steam Routing
router.register(r'steam-profile', SteamProfilesViewSet, basename = "steam-profile")

urlpatterns = router.urls