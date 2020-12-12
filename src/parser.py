from datetime import datetime
import aiohttp
import json
import numpy as np
from googlesearch import search
from src.settings import API_KEY, API_HOST, API_HOST_PICS, LANGUAGE, IDS_PATH
import emoji

top_5000_ids = []


async def search_film_links(film_name):
    ivi_link = next(search(f"ivi {film_name}"))
    netflix_link = next(search(f"netflix {film_name}"))
    if "netflix.com" not in netflix_link:
        netflix_link = None
    if "ivi.ru" not in ivi_link:
        ivi_link = None
    return (ivi_link, netflix_link)


def read_ids():
    with open(IDS_PATH) as f:
        for line in f:
            top_5000_ids.append(line)


def get_random_film():
    return np.random.choice(top_5000_ids, 1)[0]


async def get_provider_link(film_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{API_HOST}movie/{film_id}/watch/providers?api_key={API_KEY}"
            f"&language={LANGUAGE}"
        ) as response:
            if response.status != 200:
                return None
            data = await response.text()
            providers_list = json.loads(data)
            if providers_list["results"] is not None:
                if providers_list["results"].get("RU") is not None:
                    return providers_list["results"].get("RU").get("link")


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
    if film.get("poster_path") is None:
        return
    poster = await get_picture(film.get("poster_path"))
    return poster


async def get_film_full(film):
    if film is None:
        return None
    data = {}
    data["id"] = film.get("id")
    data["genres"] = film.get("genres")
    data["title"] = film.get("original_title")
    data["vote"] = film.get("vote_average")
    data["year"] = "--"
    data["production_countries"] = film.get("production_countries")[:1]
    if film.get("release_date") is not None:
        try:
            data["year"] = datetime.strptime(film.get("release_date"), "%Y-%m-%d").year
        except Exception:
            pass
    data["overview"] = film.get("overview")
    genres = []
    if data["genres"] is not None:
        for genre in data["genres"][:3]:
            genres.append(genre["name"])
    genres = ", ".join(genres)
    tmdb = await get_provider_link(data["id"])
    ivi, netflix = await search_film_links(data["title"])
    countries = [it["name"] for it in data["production_countries"]]
    countries_str = ", ".join(countries) + " "
    result = (
        f"{emoji.emojize(':movie_camera:')}{data['title']}({data['year']})\n"
        f"{countries_str}\n{genres}\n"
        f"⭐{data['vote']}\n"
        f"{data['overview']}"
    )

    if data["title"] is not None:
        return result, tmdb, ivi, netflix


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
            if response.status != 200:
                return None
            data = await response.read()
            return data
