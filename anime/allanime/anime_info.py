from pydantic import BaseModel
from typing import List, Optional
import requests
import json

class Show:
    def __init__(self, id: str, name: str, english_name: str, native_name: str, thumbnails: List[str], description: str, genres: List[str]) -> None:
        self.id = id
        self.name = name
        self.english_name = english_name
        self.native_name = native_name
        self.thumbnails = thumbnails
        self.description = description
        self.genres = genres

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            data["_id"],
            data["name"],
            data["englishName"],
            data["nativeName"],
            data["thumbnails"],
            data["description"],
            data["genres"]
        )


class Data:
    def __init__(self, show: Show) -> None:
        self.show = show

    @classmethod
    def from_json(cls, data: dict):
        return cls(Show.from_json(data["show"]))


class Showres:
    def __init__(self, data: Data) -> None:
        self.data = data

    @classmethod
    def from_json(cls, data: dict):
        return cls(Data.from_json(data["data"]))

def parser(animeid):
    json_data = requests.get(f"https://api.allanime.to/allanimeapi?variables=%7B%22_id%22%3A%22{animeid}%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22259ae45c19ceff2f855215bb82d377fe7b0ab661f9abcd41538bda935e9cb299%22%7D%7D").text
    parsed_data = json.loads(json_data)
    showres = Showres.from_json(parsed_data)
    return {
        "id": showres.data.show.id,
        "name": showres.data.show.name,
        "native_name": showres.data.show.native_name,
        "description": showres.data.show.description,
        "thumbnails": showres.data.show.thumbnails,
        "genres": showres.data.show.genres
    }

def main(animeid):
    return parser(animeid) 
