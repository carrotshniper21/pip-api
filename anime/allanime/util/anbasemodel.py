from typing import List, Optional, Dict
from pydantic import BaseModel 


class AnimeSearch(BaseModel):
    query: str
    translation_type: str


class AnimeId(BaseModel):
    anime_id: str


class EpisodeInfo(BaseModel):
    anime_id: str
    episode: str


class SourceUrl(BaseModel):
    sourceUrl: str
    priority: float
    sourceName: str
    type: str
    className: Optional[str]
    streamerId: str
    downloads: Optional[Dict[str, str]]
    mobile: Optional[Dict[str, str]]
    sandbox: Optional[str]


class EpisodeData(BaseModel):
    episodeString: str
    sourceUrls: List[SourceUrl]


class ApiResponse(BaseModel):
    data: Optional[Dict[str, EpisodeData]]


class AnimeSearchResult(BaseModel):
    id: Optional[str]
    name: Optional[str]
    native_name: Optional[str]
    description: Optional[str]
    thumbnails: Optional[List[str]]
    genres: Optional[List[str]]

class Episodes(BaseModel):
    sub: List[str]
    dub: List[str]
    raw: List

class Download(BaseModel):
    sourceName: str
    downloadUrl: str


class Mobile(BaseModel):
    sourceName: str
    downloadUrl: str


class Source(BaseModel):
    sourceUrl: str
    priority: float
    sourceName: str
    type: str
    className: str
    streamerId: str
    downloads: Optional[Download]
    mobile: Optional[Mobile]


class AnimeEpResult(BaseModel):
    __root__: List[Source]

