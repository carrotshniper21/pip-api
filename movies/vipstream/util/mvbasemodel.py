from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

class Source(BaseModel):
    file: Optional[str] = None
    type: Optional[str] = None


class Track(BaseModel):
    file: Optional[str] = None
    default: Optional[bool] = False
    kind: Optional[str] = None
    label: Optional[str] = None


class ModelItem1(BaseModel): 
    server: Optional[int] = None
    sources: Optional[List[Source]]
    tracks: Optional[List[Track]]


class ModelItem2(BaseModel):
    server: Optional[int] = None
    sources: Optional[List[Source]]
    tracks: Optional[List[Track]]


class Original(BaseModel):
    file: Optional[str] = None
    label: Optional[str] = None
    type: Optional[str] = None


class Result(BaseModel):
    Original: Optional[Original] = None


class ModelItem3(BaseModel):
    message: Optional[str] = None
    result: Optional[Result] = None
    status: Optional[str] = None
    token: Optional[str] = None
    type: Optional[str] = None

class FilmModel(BaseModel):
    image: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    id: Optional[str] = None
    release_date: Optional[str] = None
    casts: Optional[List[str]] = None
    duration: Optional[str] = None
    country: Optional[str] = None


class FilmResponse(BaseModel):
    __root__: List[FilmModel]

class ShowModel(BaseModel):
    image: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    id: Optional[str] = None
    release_date: Optional[str] = None
    casts: Optional[List[str]] = None
    duration: Optional[str] = None
    country: Optional[str] = None


class ShowResponse(BaseModel):
    __root__: List[ShowModel]

def main(data1, data2, data3):
    model_item1 = ModelItem1.parse_obj(data1)
    model_item2 = ModelItem2.parse_obj(data2)
    model_item3 = ModelItem3.parse_obj(data3)
    return (model_item1, model_item2, model_item3)
