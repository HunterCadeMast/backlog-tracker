from rest_framework.routers import DefaultRouter
from steam.views import SteamLinkViewSet, SteamUnlinkViewSet, SteamCallbackViewSet, SteamSyncViewSet

router = DefaultRouter()
router.register

router.register(r'link/', SteamLinkViewSet, basename = 'steam_link')
router.register(r'unlink/', SteamUnlinkViewSet, basename = 'steam_unlink')
router.register(r'callback/', SteamCallbackViewSet, basename = 'steam_callback')
router.register(r'sync/', SteamSyncViewSet, basename = 'steam_sync')

urlpatterns = router.urls