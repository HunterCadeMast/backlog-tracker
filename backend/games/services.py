from django.conf import settings
from django.core.cache import cache
from difflib import SequenceMatcher
from games.models import Games
import requests
import re

ACCESS_TOKEN = 'igdb_access_token'

def fetch_igdb_access_token():
    igdb_token = cache.get(ACCESS_TOKEN)
    if igdb_token:
        return igdb_token
    else:
        response = requests.post('https://id.twitch.tv/oauth2/token', data = {'client_id': settings.IGDB_CLIENT_ID, 'client_secret': settings.IGDB_CLIENT_SECRET, 'grant_type': 'client_credentials'}, timeout = 10)
        response.raise_for_status()
        igdb_token = response.json()['access_token']
        cache.set(ACCESS_TOKEN, igdb_token, timeout = 60 * 60 * 24)
        return igdb_token
    
def request_game_info(endpoint: str, body: str):
    igdb_token = fetch_igdb_access_token()
    headers = {
        'Client-ID': settings.IGDB_CLIENT_ID,
        'Authorization': f'Bearer {igdb_token}',
        'Accept': 'application/json',
    }
    response = requests.post(f'{settings.IGDB_BASE_URL}/{endpoint}', data = body, headers = headers, timeout = 10)
    response.raise_for_status()
    return response.json()

def fetch_game_info(id: int):
    body = f'''
        fields
            id,
            name,
            cover.url,
            summary,
            first_release_date,
            rating,
            genres.name,
            platforms.name,
            involved_companies.developer,
            involved_companies.publisher,
            involved_companies.company.name,
            franchises.name,
            collections.name;
        where id = {id};
        limit 1;
    '''
    results = request_game_info("games", body)
    if results:
        return results[0]
    else:
        return None

def specific_game_search(title: str):
    title = title.replace('"', '\\"')
    body = f'''
        search "{title}";
        fields
            id,
            name,
            cover.url,
            summary,
            first_release_date,
            rating,
            genres.name,
            platforms.name,
            involved_companies.developer,
            involved_companies.publisher,
            involved_companies.company.name,
            franchises.name,
            collections.name;
        limit 100;
    '''
    return request_game_info('games', body)

def broad_game_search(title: str):
    title = title.replace('"', '\\"')
    body = f'''
        fields
            id,
            name,
            cover.url,
            summary,
            first_release_date,
            rating,
            genres.name,
            platforms.name,
            involved_companies.developer,
            involved_companies.publisher,
            involved_companies.company.name,
            franchises.name,
            collections.name;
        where name ~* "{title}" | franchises.name ~* "{title}" | collections.name ~* "{title}";
        limit 100;
    '''
    return request_game_info('games', body)

def normalize_titles(title: str) -> str:
    title = title.lower()
    title = re.sub(r'[^a-z0-9 ]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def fuzzy_scoring(title: str, query: str, rating: float | None):
    title = normalize_titles(title)
    query = normalize_titles(query)
    score = 0
    if title == query:
        score += 100
    elif title.startswith(query):
        score += 80
    elif f' {query}' in title:
        score += 60
    elif query in title:
        score += 40
    score += SequenceMatcher(None, title, query).ratio() * 30
    if rating:
        score += min(rating, 100) * 0.2
    score -= abs(len(title) - len(query)) * 0.5
    return score

def ranking(games, query):
    return sorted(games, key = lambda x: fuzzy_scoring(x['name'], query, x.get('rating')), reverse = True)

def request_game_info_by_name(title: str):
    title = title.strip()
    if len(title) < 2:
        return []
    local_games = list(Games.objects.filter(game_title__icontains = title).values('igdb_id', 'game_title', 'average_rating', 'cover_artwork_link', 'summary')[:50])
    local_results = [
        {
            'id': game['igdb_id'],
            'name': game['game_title'],
            'rating': game['average_rating'],
            'cover': {'url': game['cover_artwork_link']} if game['cover_artwork_link'] else None,
            'summary': game['summary'],
        }
        for game in local_games
    ]
    igdb_results = []
    try:
        igdb_results += specific_game_search(title)
        igdb_results += broad_game_search(title)
    except Exception as exception:
        print(f"IGDB search failed because {exception}!")
    seen = set()
    total_results = []
    for game in igdb_results + local_results:
        game_id = game.get('id')
        if game_id is None or game_id not in seen:
            if game_id is not None:
                seen.add(game_id)
            total_results.append(game)
    return ranking(total_results, title)
