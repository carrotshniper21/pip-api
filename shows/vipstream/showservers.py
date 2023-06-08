import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Optional, Dict, Any


class ShowServer(BaseModel):
    ServerName: Optional[str]
    LinkID: Optional[str]


class ShowServers:
    """
    Finds show servers, and returns server ids
    """

    def __init__(self, url, showid):
        self.url = url
        self.showid = showid 

    async def serverCallback(self, soup: BeautifulSoup) -> list[Dict[str, Any]]:
        elementDiv = soup.find_all("li", {"class": "nav-item"})
        servers = [
            ShowServer(
                ServerName=server.find("span").text,
                LinkID=server.find("a").get("data-id"),
            ).dict()
            for server in elementDiv
        ]

        return servers

    async def processServers(self, serverResults: str) -> list[Dict[str, Any]]:
        soup = BeautifulSoup(serverResults, "html.parser")
        servers = await self.serverCallback(soup)
        return servers

    async def main(self) -> dict[str, list[Dict[str, Any]]]:
        async with httpx.AsyncClient() as client:
            serverResults = await client.get(
                f"{self.url}/ajax/v2/episode/servers/{self.showid}/#servers-list", timeout=10
            )
            servers = await self.processServers(serverResults.text)
            return {"servers": servers}
