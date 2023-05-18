import json
import requests
from bs4 import BeautifulSoup
from movies.vipstream.extractors.servers import main as servers
from movies.vipstream.util.show_info import main as show_info

root = "https://vipstream.tv"


class FilmFinder:
    """
    Finds film details, parses data and returns embed links
    """

    def __init__(self, base_url="https://vipstream.tv", provider="Vidcloud"):
        self.base_url = base_url
        self.provider = provider

    @staticmethod
    def display_films(film_details):
        films = [{
            "id": film.find("a").get("href"),
            "title": film.find("a").get("title")
        } for film in film_details]
        return films

    def parse_data(self, film_info):
        films = [
            {
                "servers": film.find("span").text,
                "data-id": film.find("a").get("data-linkid"),
            }
            for film in film_info
        ]
        provider_links = []
        for film in films:
            r = requests.get(
                f"{self.base_url}/ajax/sources/{film['data-id']}", timeout=10
            ).text
            links = json.loads(r)
            provider_links.append(links)
        return provider_links

    @staticmethod
    def get_embed_link(provider_links):
        sources = servers(provider_links)
        return sources

    def main(self, query):
        movie_page = requests.get(
            f"{self.base_url}/ajax/movie/episodes/{query.split('-')[-1]}",
            timeout=10,
        ).text
        soup = BeautifulSoup(movie_page, "html.parser")
        film_info = soup.find_all("li", attrs={"class": "nav-item"})
        provider_links = self.parse_data(film_info)
        film_sources = self.get_embed_link(provider_links)
        return film_sources, provider_links


class FilmAPI:
    def get_sources(query: str):
        finder = FilmFinder()
        film_sources, provider_links = finder.main(query)
        films = [provider_links, film_sources[0], film_sources[1], film_sources[2]]
        return films

    def get_film_data(query: str):
        finder = FilmFinder()
        movie_results = requests.get(
                f"{root}/search/{query.replace(' ', '-')}", timeout=10
        ).text
        soup = BeautifulSoup(movie_results, "html.parser")
        film_details = soup.find_all("div", {"class": "film-detail"})
        film_data = finder.display_films(film_details)
        films = []
        for film in film_data:
            if film["id"].startswith("/movie"):
                films.append(show_info(film["id"], film["title"]))
        return films
