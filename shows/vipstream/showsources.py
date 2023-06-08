import json
import httpx
from pydantic import BaseModel
from typing import Optional
import re

from util.decrypter import dechiper


class Source(BaseModel):
    File: Optional[str]
    Type: Optional[str]


class Track(BaseModel):
    File: Optional[str]
    Label: Optional[str]
    Kind: Optional[str]
    Default: Optional[bool] 


class ShowSource(BaseModel):
    Sources: Optional[list[Source]]
    Tracks: Optional[list[Track]] 
    Server: Optional[int]


class ShowSources:
    """
    Fetches show sources from serverIds, and returns streaming links along with subtitles
    """

    def __init__(self, url, serverid):
        self.url = url
        self.server = serverid

    async def sourcesCallback(
        self, providerLink: str, embedType: str, embedId: str
    ) -> list[dict[str, ShowSource]]:
        async with httpx.AsyncClient() as client:
            headers = {"X-Requested-With": "XMLHttpRequest"}
            sources = await client.get(
                f"{providerLink}/ajax/embed-{embedType}/getSources?id={embedId}",
                headers=headers,
                timeout=10,
            )

            ShowEncryptedSources = await client.get(
                f"{providerLink}/ajax/embed-{embedType}/getSources?id={embedId}",
                headers=headers,
                timeout=10,
            )
            ShowEncryptedSources = json.loads(ShowEncryptedSources.text)
            ShowDecryptedSources = await dechiper(ShowEncryptedSources["sources"])
            ShowEncryptedSources["sources"] = ShowDecryptedSources
            sources = ShowSource(
                Sources=[], Tracks=[], Server=ShowEncryptedSources["server"]
            )

            for source in ShowEncryptedSources["sources"]:
                file = source.get("file")
                type = source.get("type")
                sources.Sources.append(Source(File=file, Type=type))

            for track in ShowEncryptedSources["tracks"]:
                file = track.get("file")
                label = track.get("label")
                kind = track.get("kind")
                default = track.get("default")
                sources.Tracks.append(Track(File=file, Label=label, Kind=kind, Default=default)) 

        return [sources.dict()]

    async def processSources(self, embedLink: str) -> list[dict[str, ShowSource]]:
        providerLinkRegex = re.compile("(https?://[^\s/]+)")
        embedRegex = re.compile("embed-(\d+)/([\w-]+)\??")
        providerLink = providerLinkRegex.findall(embedLink)[0]
        embedMatches = embedRegex.findall(embedLink)
        embedType = embedMatches[0][0]
        embedId = embedMatches[0][1]

        sources = await self.sourcesCallback(providerLink, embedType, embedId)
        return sources

    async def main(self) -> dict[str, list[dict[str, ShowSource]]]:
        async with httpx.AsyncClient() as client:
            providerInfo = await client.get(
                f"{self.url}/ajax/sources/{self.server}", timeout=10
            )
            embedLink = json.loads(providerInfo.text)["link"]
            sources = await self.processSources(embedLink)
            return {"sources": sources}
