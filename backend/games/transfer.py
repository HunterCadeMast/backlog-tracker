from games.models import Games, Developers, Publishers, Genres, Platforms, Franchises, Series, GameSpecificDevelopers, GameSpecificPublishers, GameSpecificGenres, GameSpecificPlatforms, GameSpecificFranchises, GameSpecificSeries
from datetime import datetime

def games_database_transfer(data):
    cover_url = None
    cover = data.get('cover')
    if cover and cover.get('url'):
        cover_url = cover['url'].replace('t_thumb', 't_cover_big')
    release_date = None
    if data.get('first_release_date'):
        release_date = datetime.fromtimestamp(data['first_release_date'])
    rating = None
    if data.get('rating') is not None:
        rating = int(data['rating'])
    game, _ = Games.objects.update_or_create(
        igdb_id = data['id'], 
        defaults = {
            'game_title': data.get('name', ''),
            'cover_artwork_link': cover_url,
            'release_date': release_date, 
            'average_rating': rating, 
        }
    )
    for igdb_involved_companies in data.get('involved_companies', []):
        company = igdb_involved_companies.get('company')
        if not company:
            continue
        company_name = company.get('name')
        if not company_name:
            continue
        if igdb_involved_companies.get('developer'):
            developer, _ = Developers.objects.get_or_create(label = company_name)
            GameSpecificDevelopers.objects.get_or_create(game_id = game, developer_id = developer)
        if igdb_involved_companies.get('publisher'):
            publisher, _ = Publishers.objects.get_or_create(label = company_name)
            GameSpecificPublishers.objects.get_or_create(game_id = game, publisher_id = publisher)
    for igdb_genre in data.get('genres', []):
        name = igdb_genre.get('name')
        if not name:
            continue
        genre, _ = Genres.objects.get_or_create(label = name)
        GameSpecificGenres.objects.get_or_create(game_id = game, genre_id = genre)
    for igdb_platform in data.get('platforms', []):
        name = igdb_platform.get('name')
        if not name:
            continue
        platform, _ = Platforms.objects.get_or_create(label = name)
        GameSpecificPlatforms.objects.get_or_create(game_id = game, platform_id = platform)
    for igdb_franchise in data.get('franchises', []):
        name = igdb_franchise.get('name')
        if not name:
            continue
        franchise, _ = Franchises.objects.get_or_create(label = name)
        GameSpecificFranchises.objects.get_or_create(game_id = game, franchise_id = franchise)
    for igdb_series in data.get('collections', []):
        name = igdb_series.get('name')
        if not name:
            continue
        series, _ = Series.objects.get_or_create(label = name)
        GameSpecificSeries.objects.get_or_create(game_id = game, series_id = series)
    return game