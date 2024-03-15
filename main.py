from subtitles import opensubtitles, subscene
from fastapi import FastAPI

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
        "intro": "Welcome to pip-api <3",
        "documentation": "http://localhost:5000/docs"
    }

@app.get("/subtitles/scene/search_subtitles")
async def search_scene_subs(q: str):
    return await subscene.search_subtitles(q)

@app.get("/subtitles/scene/download_subtitle")
async def get_sub_sources(url: str):
    return await subscene.download_subtitle(url)

@app.get("/subtitles/open/search_subtitles")
async def search_open_subs(q: str): 
    return await opensubtitles.search_subtitles(q)

@app.get("/subtitles/open/download_subtitle")
async def parse_url(url: str): 
    return await opensubtitles.download_subtitle(url)
