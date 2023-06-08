from fastapi import FastAPI
from typing import Any
from films.vipstream.filmsearch import FilmSearch, FilmSearcher
from films.vipstream.filmservers import FilmServer, FilmServers
from films.vipstream.filmsources import FilmSource, FilmSources
from shows.vipstream.showsearch import ShowSearch, ShowSearcher
from shows.vipstream.showseasons import ShowSeason, ShowSeasons
from shows.vipstream.showservers import ShowServer, ShowServers
from shows.vipstream.showsources import ShowSource, ShowSources
from util.cache import cache_data

app = FastAPI(
    title="pipebomb",
    description="Pipebomb is a RESTful API designed for media serving",
    version="0.0.2",
)


@app.get("/", description="Home Page", summary="Home Page", tags=["Home"])
async def home() -> Any | dict[str, str]:
    return {
        "intro": "Welcome to pipebomb",
        "documentation": "https://pipebomb.bytecats.codes/docs",
    }


@app.get(
    "/films/vip/search",
    description="Search for films by query",
    summary="Search for films",
    tags=["Films"],
    response_model=dict[str, list[FilmSearch]],
)
async def film_search(query: str) -> Any | dict[str, list[FilmSearch]]:
    searcher = FilmSearcher("https://vipstream.tv", query)
    return await cache_data(f"film_search_{query}", searcher.main)


@app.get(
    "/films/vip/servers",
    description="Fetch film servers by film ID",
    summary="Fetch film servers",
    tags=["Films"],
    response_model=dict[str, list[FilmServer]],
)
async def film_servers(filmid: str) -> Any | dict[str, list[FilmServer]]:
    servers = FilmServers("https://vipstream.tv", filmid)
    return await cache_data(f"film_servers{filmid}", servers.main)


@app.get(
    "/films/vip/sources",
    description="Fetch film sources by server ID",
    summary="Fetch film sources",
    tags=["Films"],
    response_model=dict[str, list[FilmSource]],
)
async def film_sources(serverid: str) -> Any | dict[str, list[FilmSource]]:
    sources = FilmSources("https://vipstream.tv", serverid)
    return await cache_data(f"film_sources{serverid}", sources.main)


@app.get(
    "/series/vip/search",
    description="Search for shows by query",
    summary="Search for shows",
    tags=["Series"],
    response_model=dict[str, list[ShowSearch]],
)
async def show_search(query: str) -> Any | dict[str, list[ShowSearch]]:
    searcher = ShowSearcher("https://vipstream.tv", query)
    return await cache_data(f"show_search_{query}", searcher.main)


@app.get(
    "/series/vip/seasons",
    summary="Fetch show seasons and episodes",
    description="Fetch show seasons and episodes by show ID",
    tags=["Series"],
    response_model=dict[str, list[dict[str, ShowSeason]]],
)
async def show_seasons(showid: str) -> Any | dict[str, list[dict[str, ShowSeason]]]:
    seasons = ShowSeasons("https://vipstream.tv", showid)
    return await cache_data(f"show_seasons_{showid}", seasons.main)


@app.get(
    "/series/vip/servers",
    description="Fetch show servers by episode ID",
    summary="Fetch show servers",
    tags=["Series"],
    response_model=dict[str, list[ShowServer]],
)
async def show_servers(episodeid: str) -> Any | dict[str, list[ShowServer]]:
    servers = ShowServers("https://vipstream.tv", episodeid)
    return await cache_data(f"show_servers{episodeid}", servers.main)

@app.get(
    "/series/vip/sources",
    description="Fetch show sources by server ID",
    summary="Fetch show sources",
    tags=["Series"],
    response_model=dict[str, list[ShowSource]],
)
async def show_sources(serverid: str) -> Any | dict[str, list[ShowSource]]:
    sources = ShowSources("https://vipstream.tv", serverid)
    return await cache_data(f"show_sources{serverid}", sources.main)

