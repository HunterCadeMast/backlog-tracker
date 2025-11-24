from rest_framework import routers
from profiles.views import ProfilesViewSet, OAuthenticationTokensViewSet, APIKeysViewSet, SteamProfilesViewSet
from games.views import GamesViewSet, DevelopersViewSet, GameSpecificDevelopersViewSet, PublishersViewSet, GameSpecificPublishersViewSet, GenresViewSet, GameSpecificGenresViewSet, PlatformsViewSet, GameSpecificPlatformsViewSet, FranchisesViewSet, GameSpecificFranchisesViewSet, SeriesViewSet, GameSpecificSeriesViewSet
from logs.views import LogsViewSet, LogTagsViewSet
from playlists.views import PlaylistsViewSet, PlaylistLogsViewSet
from recommendations.views import RecommendationsViewSet

router = routers.SimpleRouter()
router.register(r'profile', ProfilesViewSet, basename = "profile")
urlpatterns = router.urls