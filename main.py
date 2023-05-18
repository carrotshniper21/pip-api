from lightnovels.readlightnovels import light_novel
from movies.vipstream.pip_api_films import FilmAPI
from movies.vipstream.pip_api_shows import ShowAPI
from subtitles.opensubtitles import opensubtitles
from movies.vipstream.util import mvbasemodel
from anime.allanime.util import anbasemodel
from subtitles.subscene import subscene
from anime.allanime import aniscray
from util.cache import cache_data
from fastapi import FastAPI
from typing import List

# pip-api/main.py
# main branch

app = FastAPI(
    title="Pip API",
    description="""
Pip API is a RESTful API designed for films and shows. 🎥
## Films/Shows
You can retrieve film/show data by making API calls to endpoints.
## Users
Users will be able to fetch show and film data, as well as stream sources.
""",
    version="0.0.1",
)

@app.get("/")
async def get_routes():
    return {
        "intro": "Welcome to pip-api. UWU",
        "documentation": "http://pipebomb.bytecats.codes:8000/docs"
    }

scraper = aniscray.AnimeScraper()

@app.post("/anime/all/search_anime", response_model=List[anbasemodel.AnimeSearchResult])
async def search_anime(anime_search: anbasemodel.AnimeSearch):
    return await cache_data(f"anime_search_{anime_search.query}", scraper.search_anime, anime_search.query)

@app.post("/anime/all/get_episodes/", response_model=anbasemodel.Episodes)
async def get_episodes(anime_id: anbasemodel.AnimeId):
    episodes = await cache_data(f"anime_episodes_{anime_id.anime_id}", scraper.get_episodes, anime_id.anime_id)
    return anbasemodel.Episodes(**episodes)

@app.post("/anime/all/get_episode_url/", response_model=anbasemodel.AnimeEpResult)
async def get_episode_url(episode_info: anbasemodel.EpisodeInfo):
    return await cache_data(f"anime_ep_url_{episode_info.anime_id}_{episode_info.episode}", scraper.get_episode_url, episode_info.anime_id, episode_info.episode)

@app.get("/films/vip/search", response_model=mvbasemodel.FilmResponse)
async def get_film(q: str):
    return await cache_data(f"films_{q}", FilmAPI.get_film_data, q)

@app.get("/films/vip/source")
async def get_sources(q: str):
    return await cache_data(f"films_sources_{q}", FilmAPI.get_sources, q)

@app.get("/series/vip/search", response_model=mvbasemodel.ShowResponse)
async def get_shows(q: str):
    return await cache_data(f"shows_{q}", ShowAPI.get_show_data, q)

@app.get("/series/vip/id")
async def get_show_info(q: str):
    return await cache_data(f"shows_info_{q}", ShowAPI.get_sources, q)

@app.get("/series/vip/episode")
async def get_episode_id(q: str):
    return await cache_data(f"shows_episode_id_{q}", ShowAPI.get_episodes, q)

@app.get("/lightnovel/read/search_novels")
async def search_novels(q: str):
    return await light_novel.novel_searcher(q)

@app.get("/lightnovel/read/novel_info")
async def get_novel_info(q: str):
    return await light_novel.novel_info(q)

@app.get("/lightnovel/read/chapters")
async def choose_novel_chapter(q: str):
    return await light_novel.novel_chapter_chooser(q)

@app.get("/lightnovel/read/chapter_content")
async def get_chapter(q: str):
    return await light_novel.get_chapter_text(q)

@app.get("/subtitles/scene/search_subtitles")
async def search_subs(q: str):
    return await subscene.search_subtitles(q)

@app.get("/subtitles/scene/get_sub_url")
async def get_sub_url(sub_id: str):
    return await subscene.parse_url(sub_id)

@app.get("/subtitles/scene/search_subtitles")
async def get_sub_sources(sub_url: str):
    return await subscene.sub_file(sub_url)

@app.get("/subtitles/open/search_subtitles")
async def get_xml_data(lang_code: str, media_name: str): 
    return await opensubtitles.get_xml_data(lang_code, media_name)     

@app.get("/subtitles/open/search_subtitles")
async def parse_url(q: str): 
    return await opensubtitles.parse_url(q)
