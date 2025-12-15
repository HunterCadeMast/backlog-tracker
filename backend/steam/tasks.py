from django.utils import timezone
from django.core.cache import cache
from steam.models import SteamProfiles
from celery import shared_task
from steam.services import fetch_steam_player, fetch_steam_games
from games.models import Games

@shared_task(bind = True, autoretry_for = Exception, retry_backoff = 60, retry_kwargs = {'max_retries': 5})
def auto_sync_steam(self, profile_id):
    profile = SteamProfiles.objects.get(id = profile_id)
    key = f'steam_autosync:{profile.steam_id}'
    if not cache.get(key):
        data = fetch_steam_player(profile.steam_id)
        profile.steam_username = data['personaname']
        profile.steam_avatar_link = data['avatarfull']
        profile.steam_public_profile = (data['communityvisibilitystate'] == 3)
        owned_games = fetch_steam_games(profile.steam_id)
        for game in owned_games:
            Games.objects.update_or_create(igdb_id = game['appid'], defaults = {'game_title': game['name'], 'completion_time': game.get('playtime_forever', 0)})
        profile.last_fetched = timezone.now()
        profile.save(update_fields = ['steam_username', 'steam_avatar_link', 'steam_public_profile', 'last_fetched'])
        cache.set(key, True, timeout = 300)

@shared_task
def auto_sync_all():
    for profile in SteamProfiles.objects.filter(auto_sync_games = True):
        auto_sync_steam.delay(profile.id)