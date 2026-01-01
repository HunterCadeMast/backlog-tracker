from games.models import Games, Developers, Publishers, Genres, Platforms, Franchises, Series, GameSpecificDevelopers, GameSpecificPublishers, GameSpecificGenres, GameSpecificPlatforms, GameSpecificFranchises, GameSpecificSeries
from datetime import datetime

def games_database_transfer(data):
    game, _ = Games.objects.update_or_create(
        igdb_id = data['id'], 
        defaults = {
            'game_title': data['name'],
            'cover_artwork_link': data['cover']['url'].replace('t_thumb', 't_cover_big') if data.get('cover') else None,
            'release_date': datetime.fromtimestamp(data['first_release_date']) if data.get('first_release_date') else None, 
            'average_rating': int(data.get('rating', 0)) if data.get('rating') else None, 
        }
    )
    for igdb_involved_companies in data.get('involved_companies', []):
        if igdb_involved_companies.get('developer'):
            developer, _ = Developers.objects.get_or_create(label = igdb_involved_companies['company']['name'])
            GameSpecificDevelopers.objects.get_or_create(game_id = game, developer_id = developer)
        if igdb_involved_companies.get('publisher'):
            publisher, _ = Publishers.objects.get_or_create(label = igdb_involved_companies['company']['name'])
            GameSpecificPublishers.objects.get_or_create(game_id = game, publisher_id = publisher)
    for igdb_genre in data.get('genres', []):
        genre, _ = Genres.objects.get_or_create(label = igdb_genre['name'])
        GameSpecificGenres.objects.get_or_create(game_id = game, genre_id = genre)
    for igdb_platform in data.get('platforms', []):
        platform, _ = Platforms.objects.get_or_create(label = igdb_platform['name'])
        GameSpecificPlatforms.objects.get_or_create(game_id = game, platform_id = platform)
    for igdb_franchise in data.get('franchises', []):
        franchise, _ = Franchises.objects.get_or_create(label = igdb_franchise['name'])
        GameSpecificFranchises.objects.get_or_create(game_id = game, franchise_id = franchise)
    for igdb_series in data.get('collections', []):
        series, _ = Series.objects.get_or_create(label = igdb_series['name'])
        GameSpecificSeries.objects.get_or_create(game_id = game, series_id = series)
    return game