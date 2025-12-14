from django.urls import path
from steam.views import SteamProfiles, SteamLinkViewSet, SteamUnlinkViewSet, SteamCallbackViewSet, SteamSyncViewSet

urlpatterns = [
    path('link/', SteamLinkViewSet.as_view(), name = 'steam_link'),
    path('unlink/', SteamUnlinkViewSet.as_view(), name = 'steam_unlink'),
    path('callback/', SteamCallbackViewSet.as_view(), name = 'steam_callback'),
    path('sync/', SteamSyncViewSet.as_view(), name = 'steam_sync'),
]