import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Optional

class Episode(BaseModel):
    Title: Optional[str]
    EpisodeID: Optional[str]

class ShowSeason(BaseModel):
    SeasonName: Optional[str]
    SeasonID: Optional[str]
    Episodes: Optional[list[Episode]]

class ShowSeasons:
    """
    Fetches show seasons from showids
    """
    def __init__(self, url, showid):
        self.url = url
        self.showid = showid

    async def episodeCallback(self, seasonID: str) -> list[Episode]:
        async with httpx.AsyncClient() as client:
            episodes = []
            episodeResults = await client.get(
                f"{self.url}/ajax/v2/season/episodes/{seasonID}", timeout=10
            )
            soup = BeautifulSoup(episodeResults.text, "html.parser")
            episodeDiv = soup.find_all("a", {"class": "eps-item"})
            for episode in episodeDiv:
                episodes.append(Episode(Title=episode["title"], EpisodeID=episode["data-id"]))
            return episodes

    async def seasonCallback(self, soup: BeautifulSoup) -> list[dict[str, ShowSeason]]:
        seasons = []
        for season in soup.find_all("a"):
            episodes = await self.episodeCallback(season["data-id"])
            seasons.append({f"{season.text}": ShowSeason(SeasonName=season.text, SeasonID=season["data-id"], Episodes=episodes).dict()})
        return seasons

    async def processSeasons(self, seasonResults: str) -> list[dict[str, ShowSeason]]:
        soup = BeautifulSoup(seasonResults, "html.parser")
        seasons = await self.seasonCallback(soup)
        return seasons

    async def main(self):
        async with httpx.AsyncClient() as client:
            seasonResults = await client.get(
                f"{self.url}/ajax/v2/tv/seasons/{self.showid}", timeout=10
            )
            seasons = await self.processSeasons(seasonResults.text)
            return {"seasons": seasons}
