from fastapi import FastAPI
from films.vipstream.filmsearch import FilmSearch, FilmSearcher
from films.vipstream.filmservers import FilmServer, FilmServers
from films.vipstream.filmsources import FilmSource, FilmSources
from util.cache import cache_data

app = FastAPI(
    title="pipebomb",
    description="Pipebomb is a RESTful API designed for media serving",
    version="0.0.2",
)


@app.get("/", description="Home Page", summary="Home Page", tags=["Home"])
async def home():
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
async def film_search(query: str):
    searcher = FilmSearcher("https://vipstream.tv", query)
    return await cache_data(f"film_search_{query}", searcher.main)


@app.get(
    "/films/vip/servers",
    description="Fetch film servers by film ID",
    summary="Fetch film servers",
    tags=["Films"],
    response_model=dict[str, list[FilmServer]]
)
async def film_servers(filmid: str):
    servers = FilmServers("https://vipstream.tv", filmid)
    return await cache_data(f"film_servers{filmid}", servers.main)

@app.get(
    "/films/vip/sources",
    description="Fetch film sources by server ID",
    summary="Fetch film sources",
    tags=["Films"],
    response_model=dict[str, list[FilmSource]]
)
async def film_sources(serverid: str):
    sources = FilmSources("https://vipstream.tv", serverid)
    return await cache_data(f"film_sources{serverid}", sources.main)

