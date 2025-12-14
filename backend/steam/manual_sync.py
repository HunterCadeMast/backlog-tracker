from django.conf import settings
import requests

STEAM_API = 'https://api.steampowered.com'

def fetch_steam_player(steam_id):
    request = requests.get(f'{STEAM_API}/ISteamUser/GetPlayerSummaries/v2/', parameters = {'key': settings.STEAM_API_KEY, 'steam_id': steam_id}, timeout = 5)
    request.raise_for_status()
    return request.json()['response']['players'][0]

def fetch_steam_games(steam_id):
    request = requests.get(f'{STEAM_API}/IPlayerService/GetOwnedGames/v1/', parameters = {'key': settings.STEAM_API_KEY, 'steam_id': steam_id, 'include_appinfo': True}, timeout = 5)
    request.raise_for_status()
    return request.json()['response'].get('games', [])