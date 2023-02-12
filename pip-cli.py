import requests
import json

from bs4 import BeautifulSoup
from rich import print
from rich.progress import track
from utils import questionary_utils

print("""
[bold orange1]
▄▄▄▄·  ▄▄▄· ▄▄▌  ▄▄▌  .▄▄ ·      ▄▄▄·  ▄▄▄·▪  
▐█ ▀█▪▐█ ▀█ ██•  ██•  ▐█ ▀.     ▐█ ▀█ ▐█ ▄███ 
▐█▀▀█▄▄█▀▀█ ██▪  ██▪  ▄▀▀▀█▄    ▄█▀▀█  ██▀·▐█·
██▄▪▐█▐█ ▪▐▌▐█▌▐▌▐█▌▐▌▐█▄▪▐█    ▐█ ▪▐▌▐█▪·•▐█▌
·▀▀▀▀  ▀  ▀ .▀▀▀ .▀▀▀  ▀▀▀▀      ▀  ▀ .▀   ▀▀▀
[/bold orange1]""")

class FilmFinder:
    def __init__(self, base_url="https://vipstream.tv", provider="Vidcloud"):
        self.base_url = base_url
        self.provider = provider

    def get_results(self, query):
        r = requests.get(f"{self.base_url}/search/{query}")
        return r.content

    def display_films(self, film_details):
        films = [
            {"id": film.find("a").get("href"), "title": film.find("a").get("title")}
            for film in film_details
        ]
        for i, film in enumerate(films):
            print(
                f"({i + 1}): [bold magenta]{film['title']}[/bold magenta] [bold cyan]'{self.base_url}{film['id']}'[/bold cyan]"
            )
        return films

    def get_number_after_last_dash(self, s):
        parts = s.split("-")
        return int(parts[-1])

    def movie_page(self, film_data):
        film_choice = questionary_utils.text_input("Choose one NOW:").ask()
        film_choice_data = film_data[int(film_choice) - 1]
        film_choice_id = film_choice_data["id"].split("-")
        r = requests.get(f"{self.base_url}/ajax/movie/episodes/{film_choice_id[-1]}")
        return r.content

    def parse_data(self, film_info):
        films = [
            {"servers": film.find("span").text, "data-id": film.find("a").get("data-linkid")}
            for film in film_info
        ]
        for film in films:
            if self.provider == film["servers"]:
                return (film["servers"], film["data-id"], films)

    def get_embed_link(self, film_id):
        r = requests.get(f"{self.base_url}/ajax/sources/{film_id}")
        provider_info = json.loads(r.text)
        link = provider_info["link"]
        parts = link.split('/')
        provider_link = parts[0] + '//' + parts[2]
        embed_type = parts[3].replace('embed-', '')
        source_id = parts[4]
        return (provider_link, embed_type, source_id[:-3], provider_info)

    def get_stream_link(self, film_iframe):
        r = requests.get(f"{film_iframe[0]}/ajax/embed-{film_iframe[1]}/getSources?id={film_iframe[2]}", headers={"X-Requested-With": "XMLHttpRequest"})
        return r.text

    def main(self, query):
        query = query.replace(" ", "-")
        movies_results = self.get_results(query)
        soup = BeautifulSoup(movies_results, "html.parser")
        film_details = soup.find_all("div", attrs={"class": "film-detail"})
        film_data = self.display_films(film_details)
        film_choice = self.movie_page(film_data)
        soup = BeautifulSoup(film_choice, "html.parser")
        film_info = soup.find_all("li", attrs={"class": "nav-item"})
        film_id = self.parse_data(film_info)
        film_iframe = self.get_embed_link(film_id[1])
        film_sources = self.get_stream_link(film_iframe)
        print(film_data, film_id[2], film_iframe[3], film_sources)

if __name__ == "__main__":
    finder = FilmFinder()
    query = questionary_utils.text_input("Enter something NOW:").ask()
    finder.main(query)
