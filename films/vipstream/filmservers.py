import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Optional, Dict, Any


class FilmServer(BaseModel):
    ServerName: Optional[str]
    LinkID: Optional[str]


class FilmServers:
    """
    Finds film servers, and returns server ids
    """

    def __init__(self, url, filmid):
        self.url = url
        self.filmid = filmid

    async def serverCallback(self, soup: BeautifulSoup) -> list[Dict[str, Any]]:
        elementDiv = soup.find_all("li", {"class": "nav-item"})
        servers = [
            FilmServer(
                ServerName=server.find("span").text,
                LinkID=server.find("a").get("data-linkid"),
            ).dict()
            for server in elementDiv
        ]

        return servers

    async def processServers(self, serverResults: str) -> list[Dict[str, Any]]:
        """
        (self) -> list[Dict[str, Any]]
        {
            "servers": [
                {
                    "serverName": string
                    "linkID": string,
                },
                {
                    "serverName": string
                    "linkID": string
                }
            ]
        }
        """
        soup = BeautifulSoup(serverResults, "html.parser")
        servers = await self.serverCallback(soup)
        return servers

    async def main(self) -> dict[str, list[Dict[str, Any]]]:
        async with httpx.AsyncClient() as client:
            serverResults = await client.get(
                f"{self.url}/ajax/movie/episodes/{self.filmid}", timeout=10
            )
            servers = await self.processServers(serverResults.text)
            return {"servers": servers}
