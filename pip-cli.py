import json
import logging
import subprocess
from base64 import b64decode
from hashlib import md5
from Cryptodome.Cipher import AES
from flask import Flask, request
from rich.logging import RichHandler
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Rich logging implmentation not needed zoe
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
r = requests.get("https://raw.githubusercontent.com/enimax-anime/key/e4/key.txt")
SECRET = bytes(r.text, "utf-8")


class FilmFinder:
    def __init__(self, base_url="https://vipstream.tv", provider="Vidcloud"):
        self.base_url = base_url
        self.provider = provider

    # Needed for search functionality
    def get_results(self, query):
        r = requests.get(f"{self.base_url}/search/{query}")
        return r.content

    def display_films(self, film_details):
        films = [
            {"id": film.find("a").get("href"), "title": film.find("a").get("title")}
            for film in film_details
        ]
        return films

    def movie_page(self, film_data):
        film_choice_id = film_data.split("-")[-1]
        r = requests.get(f"{self.base_url}/ajax/movie/episodes/{film_choice_id}")
        return r.content

    def parse_data(self, film_info):
        films = [
            {
                "servers": film.find("span").text,
                "data-id": film.find("a").get("data-linkid"),
            }
            for film in film_info
        ]
        for film in films:
            if self.provider == film["servers"]:
                return (film["servers"], film["data-id"], films)

    def get_embed_link(self, film_id):
        r = requests.get(f"{self.base_url}/ajax/sources/{film_id}")
        provider_info = json.loads(r.text)
        link = provider_info["link"]
        parts = link.split("/")
        provider_link = parts[0] + "//" + parts[2]
        embed_type = parts[3].replace("embed-", "")
        source_id = parts[4]
        return (provider_link, embed_type, source_id[:-3], provider_info)

    def get_stream_link(self, film_iframe):
        r = requests.get(
            f"{film_iframe[0]}/ajax/embed-{film_iframe[1]}/getSources?id={film_iframe[2]}",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        return r.text

    def main(self, query):
        query = query.replace(" ", "-")
        film_choice = self.movie_page(query)
        soup = BeautifulSoup(film_choice, "html.parser")
        film_info = soup.find_all("li", attrs={"class": "nav-item"})
        film_id = self.parse_data(film_info)
        film_iframe = self.get_embed_link(film_id[1])
        film_sources = self.get_stream_link(film_iframe)
        return film_sources


class Decrypt:
    def generate_key(self, salt: bytes, *, output=48):
        key = md5(SECRET + salt).digest()
        current_key = key
        while len(current_key) < output:
            key = md5(key + SECRET + salt).digest()
            current_key += key
        return current_key[:output]

    def decipher(self, encoded_url: str):
        s1 = b64decode(encoded_url.encode("utf-8"))
        key = self.generate_key(s1[8:16])
        decrypted = AES.new(key[:32], AES.MODE_CBC, key[32:]).decrypt(s1[16:])
        decrypted = decrypted[: -decrypted[-1]].decode("utf-8", "ignore").lstrip(" ")
        return json.loads(decrypted)


class FilmAPI:
    @app.route("/film", methods=["GET"])
    def get_film():
        query = request.args.get("query")
        finder = FilmFinder()
        movies_results = finder.get_results(query)
        soup = BeautifulSoup(movies_results, "html.parser")
        film_details = soup.find_all("div", attrs={"class": "film-detail"})
        film_data = finder.display_films(film_details)
        return film_data

    @app.route("/sources", methods=["GET"])
    def get_sources():
        finder = FilmFinder()
        decrypt = Decrypt()
        query = request.args.get("query")
        film_sources = finder.main(query)
        sources_dict = json.loads(film_sources)
        sources = sources_dict["sources"]
        decrypted_link = decrypt.decipher(sources)
        new_sources_dict = {
            "sources": decrypted_link,
            "tracks": sources_dict["tracks"],
            "server": sources_dict["server"]
        }
        return json.dumps(new_sources_dict)


if __name__ == "__main__":
    app.run(debug=True)
