import asyncio
from datetime import datetime
import aiohttp
import json

API_KEY = "a72b90d6328f49462f1c6577197cf916"
API_HOST = "https://api.themoviedb.org/3/"
LANGUAGE = 'en-RU'


async def get_films_list(films):
    result = []
    for item in films[:6]:
        cur = await get_film_briefli(item)
        if cur is not None:
            result.append(cur)
    return '\n'.join(result)


async def get_film_briefli(film):
    data = {}
    data['id'] = film.get('id')
    data['genres'] = film.get('genre_ids')
    data['title'] = film.get('original_title')
    data['vote'] = film.get('vote_average')
    data['year'] = '--'
    if film.get('release_date') is not None:
        data['year'] = datetime.strptime(film.get('release_date'), '%Y-%m-%d').year
    result = (f"* {data['title']}({data['year']}) /{data[id]}\n"
              f"***{data['vote']}")
    if data['title'] is not None:
        return result


async def get_film_full(film):
    data = {}
    data['id'] = film.get('id')
    data['genres'] = film.get('genre_ids')
    data['title'] = film.get('original_title')
    data['vote'] = film.get('vote_average')
    data['year'] = '--'
    if film.get('release_date') is not None:
        data['year'] = datetime.strptime(film.get('release_date'), '%Y-%m-%d').year
    data['overview'] = film.get('overview')
    result = (f"* {data['title']}({data['year']})"
              f"***{data['vote']}")
    if data['title'] is not None:
        return result


async def get_films_by_text(query):
    async with aiohttp.ClientSession() as session:
        url = 'http://api.kinopoisk.cf/'
        async with session.get(API_HOST + f'search/movie?api_key={API_KEY}&query={query}'
                                          f'&language={LANGUAGE}') as response:
            if (response.status != 200):
                return None
            data = await response.text()
            films_list = json.loads(data)
            return films_list['results']


async def get_film_by_id(movie_id):
    async with aiohttp.ClientSession() as session:
        url = 'http://api.kinopoisk.cf/'
        async with session.get(API_HOST + f'movie/{movie_id}?api_key={API_KEY}'
                                          f'&language={LANGUAGE}') as response:
            if (response.status != 200):
                return None
            data = await response.text()
            film = json.loads(data)
            return film


async def get_trending():
    async with aiohttp.ClientSession() as session:
        url = 'http://api.kinopoisk.cf/'
        async with session.get(API_HOST + f'trending/all/week?api_key={API_KEY}'
                               ) as response:
            if (response.status != 200):
                return None
            data = await response.text()
            films_list = json.loads(data)
            return films_list['results']