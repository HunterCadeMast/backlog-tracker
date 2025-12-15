from django.conf import settings
from django.core.cache import cache
import requests

ACCESS_TOKEN = 'igdb_access_token'

def fetch_igdb_access_token():
    igdb_token = cache.get(ACCESS_TOKEN)
    if igdb_token:
        return igdb_token
    else:
        response = requests.post('https://id.twitch.tv/oauth2/token', parameters = {'client_id': settings.IGDB_CLIENT_ID, 'client_secret': settings.IGDB_CLIENT_SECRET, 'grant_type': 'client_credentials'}, timeout = 10)
        response.raise_for_status()
        igdb_token = response.json()['access_token']
        cache.set(ACCESS_TOKEN, igdb_token, timeout = 60 * 60 * 24)
        return igdb_token
    
def request_game_info(endpoint: str, body: str):
    igdb_token = fetch_igdb_access_token()
    headers = {
        'CLIENT_ID': settings.IGDB_CLIENT_ID,
        'AUTHORIZATION': igdb_token
    }
    response = requests.post(f'{settings.IGDB_BASE_URL}/{endpoint}', data = body, headers = headers, timeout = 10)
    response.raise_for_status()
    return response.json()

def request_game_info_by_name(name: str):
    body = f'''
        search "{name}";
        fields
            id,
            name,
            first_release_date,
            rating,
            cover.url,
            genres.name,
            involved_companies.company.name,
            involved_companies.publisher,
            involved_companies.developer,
            platforms.name,
            franchies.name,
            collections.name,
        limit 1;
    '''
    response = request_game_info('games', body)
    if response:
        return response[0]