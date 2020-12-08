import asyncio
from datetime import datetime
import aiohttp
import json
import numpy as np


# API_KEY = "a72b90d6328f49462f1c6577197cf916"
# API_HOST = "https://api.themoviedb.org/3/"
# API_HOST_PICS = 'https://image.tmdb.org/t/p/w500'
# LANGUAGE = "ru-RU"
top_5000_ids = []


def read_ids():
    with open('id.txt') as f:
        for line in f:
            top_5000_ids.append(line)


def get_random_film():
    return np.random.choice(top_5000_ids, 1)[0]


async def get_provider_link(film_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_HOST}movie/{film_id}/watch/providers?api_key={API_KEY}'
                               f'&language={LANGUAGE}') as response:
            if (response.status != 200):
                return None
            data = await response.text()
            providers_list = json.loads(data)
            if providers_list['results'] is not None:
                if providers_list['results'].get('RU') is not None:
                    return providers_list['results'].get('RU').get('link')


async def get_films_list(films):
    result = []
    for item in films[:6]:
        cur = await get_film_briefli(item)
        if cur is not None:
            result.append(cur)
    return "\n".join(result)


async def get_film_briefli(film):
    data = {}
    data["id"] = film.get("id")
    data["genres"] = film.get("genre_ids")
    data["title"] = film.get("original_title")
    data["vote"] = film.get("vote_average")
    data["year"] = "--"
    if film.get("release_date") is not None:
        try:
            data["year"] = datetime.strptime(film.get("release_date"), "%Y-%m-%d").year
        except Exception:
            pass

    result = f"{data['title']}({data['year']}) /id{data['id']}\n" f"⭐{data['vote']}"
    if data["title"] is not None:
        return result


async def get_film_poster(film):
    if film.get('poster_path') is None:
        return
    poster = await get_picture(film.get('poster_path'))
    return poster

async def get_film_full(film):
    data = {}
    data["id"] = film.get("id")
    data["genres"] = film.get("genres")
    data["title"] = film.get("original_title")
    data["vote"] = film.get("vote_average")
    data["year"] = "--"
    if film.get("release_date") is not None:
        try:
            data["year"] = datetime.strptime(film.get("release_date"), "%Y-%m-%d").year
        except Exception:
            pass
    data["overview"] = film.get("overview")
    genres = []
    if data['genres'] is not None:
        for genre in data['genres'][:3]:
            genres.append(genre['name'])
    genres = ', '.join(genres)
    link = await get_provider_link(data['id'])
    result = (
        f"{data['title']}({data['year']})\n"
        f"{genres}\n"
        f"⭐{data['vote']}\n"
        f"{data['overview']}") + (f"\nссылка на [TMDB]({link}" if link is not None else '')
    if data["title"] is not None:
        return result


async def get_films_by_text(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{API_HOST}search/movie?api_key={API_KEY}&query={query}"
            f"&language={LANGUAGE}"
        ) as response:
            if response.status != 200:
                return None
            data = await response.text()
            films_list = json.loads(data)
            return films_list["results"]


async def get_film_by_id(movie_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{API_HOST}movie/{movie_id}?api_key={API_KEY}" f"&language={LANGUAGE}"
        ) as response:
            if response.status != 200:
                return None
            data = await response.text()
            film = json.loads(data)
            return film


async def get_trending():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{API_HOST}trending/all/week?api_key={API_KEY}"
        ) as response:
            if response.status != 200:
                return None
            data = await response.text()
            films_list = json.loads(data)
            return films_list["results"]


async def get_picture(path):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_HOST_PICS + path) as response:
            if (response.status != 200):
                return None
            data = await response.read()
            return data