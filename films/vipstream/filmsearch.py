import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Tuple, Dict, Any, Optional
import re


class IdSplit(BaseModel):
    Type: Optional[str]
    Name: Optional[str]
    IdNum: Optional[int]


class FilmSearch(BaseModel):
    Href: Optional[str]
    Poster: Optional[str]
    Title: Optional[str]
    Description: Optional[str]
    Duration: Optional[str]
    Country: Optional[list[str]]
    Production: Optional[list[str]]
    Id: Optional[str]
    IdParts: Optional[IdSplit]
    Cast: Optional[list[str]]
    Genres: Optional[list[str]]
    Released: Optional[str]


class FilmSearcher:
    """
    Handles user queries and returns film search results
    """

    def __init__(self, url, query):
        self.url = url
        self.query = query

    async def posterCallback(self, soup: BeautifulSoup) -> str | None:
        poster = soup.find("img", {"class": "film-poster-img"})
        return poster["src"]

    async def descriptionCallback(self, soup: BeautifulSoup) -> str | None:
        elementDiv = soup.find("div", {"class": "description"})
        description = elementDiv.text.strip()
        return description

    async def releaseDateCallback(self, soup: BeautifulSoup) -> str | None:
        elementDiv = soup.find("div", {"class": "row-line"})
        elements = [element.text.strip() for element in elementDiv]
        releaseDate = elements[2]
        return releaseDate

    async def castCallback(self, soup: BeautifulSoup) -> list[str] | None:
        elementDiv = soup.find_all("div", {"class": "row-line"})
        elements = [element.text.strip() for element in elementDiv]
        elements = [e for e in elements if "Duration" not in e]
        elements = [e.strip() for e in elements]
        casts = [
            c.strip()
            for c in elements[2].replace("Casts:", "").replace("\n", "").split(",")
        ]
        return casts

    async def durationCallback(self, soup: BeautifulSoup) -> str | None:
        elementDiv = soup.find_all("div", {"class": "row-line"})
        elements = [element.text.strip() for element in elementDiv]
        duration = [e for e in elements if "Duration" in e]
        duration = duration[0].replace("Duration:", "").replace("\n", "").strip()
        duration = re.sub("(\s+)", r" ", duration)
        return duration

    async def countryCallback(self, soup: BeautifulSoup) -> list[str] | None:
        elementDiv = soup.find_all("div", {"class": "row-line"})
        elements = [element.text.strip() for element in elementDiv]
        country = [e for e in elements if "Country" in e]
        country = country[0].replace("Country:", "").replace("\n", "").strip()
        country = re.sub("(\s+)", r" ", country)
        return country.split(",")

    async def genreCallback(self, soup: BeautifulSoup) -> list[str] | None:
        elementDiv = soup.find_all("div", {"class": "row-line"})
        elements = [element.text.strip() for element in elementDiv]
        genre = [e for e in elements if "Genre" in e]
        genre = genre[0].replace("Genre:", "").replace("\n", "").strip()
        genre = re.sub("(\s+)", r" ", genre)
        return genre.split(",")

    async def productionCallback(self, soup: BeautifulSoup) -> list[str] | None:
        elementDiv = soup.find_all("div", {"class": "row-line"})
        elements = [element.text.strip() for element in elementDiv]
        production = [e for e in elements if "Production" in e]
        production = production[0].replace("Production:", "").replace("\n", "").strip()
        production = re.sub("(\s+)", r" ", production)
        return production.split(",")

    async def titleCallback(self, soup: BeautifulSoup) -> str | None:
        title = soup.find("h2", {"class": "heading-name"})
        return title.text

    async def idCallback(self, absLink: str) -> Tuple[str, IdSplit]:
        idParts = absLink.split("/")
        if len(idParts) >= 5:
            id = idParts[3] + "/" + idParts[4]
            idType = idParts[3]
            nameAndId = idParts[4].split("-")
            if len(nameAndId) > 1:
                idNum = int(nameAndId[len(nameAndId) - 1])
                idName = "-".join(nameAndId[: len(nameAndId) - 2]).replace("watch-", "")
                return id, IdSplit(Type=idType, Name=idName, IdNum=idNum)

    async def processResult(self, results: list[FilmSearch], absLink: str) -> None:
        async with httpx.AsyncClient() as client:
            filmPage = await client.get(f"{absLink}", timeout=10)
            soup = BeautifulSoup(filmPage.text, "html.parser")

            poster = await self.posterCallback(soup)
            title = await self.titleCallback(soup)
            description = await self.descriptionCallback(soup)
            duration = await self.durationCallback(soup)
            country = await self.countryCallback(soup)
            production = await self.productionCallback(soup)
            id, idParts = await self.idCallback(absLink)
            casts = await self.castCallback(soup)
            genres = await self.genreCallback(soup)
            releaseDate = await self.releaseDateCallback(soup)

            filmResponse = FilmSearch(
                Href=absLink,
                Poster=poster,
                Title=title,
                Description=description,
                Duration=duration,
                Country=country,
                Production=production,
                Id=id,
                IdParts=idParts,
                Cast=casts,
                Genres=genres,
                Released=releaseDate,
            )
            results.append(filmResponse.dict())

    async def processLink(self, filmResults: str) -> list[Dict[str, Any]]:
        results = []
        soup = BeautifulSoup(filmResults, "html.parser")
        filmDetails = soup.find_all("div", {"class": "film-detail"})
        filmIds = [film.find("a").get("href") for film in filmDetails]
        for filmId in filmIds:
            if "movie/watch" in filmId:
                await self.processResult(results, self.url + filmId)
        return results

    async def main(self) -> dict[str, list[Dict[str, Any]]]:
        async with httpx.AsyncClient() as client:
            filmResults = await client.get(
                f"{self.url}/search/{self.query.replace(' ', '-')}", timeout=10
            )
            results = await self.processLink(filmResults.text)
            return {"results": results}
