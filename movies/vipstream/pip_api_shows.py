import json
import requests
from bs4 import BeautifulSoup
from movies.vipstream.extractors.servers import main as servers
from movies.vipstream.util.show_info import main as show_info


class ShowFinder:
    def __init__(self, base_url="https://vipstream.tv", provider="Vidcloud"):
        self.base_url = base_url
        self.provider = provider

    @staticmethod
    def display_shows(show_details):
        shows = [{
            "id": show.find("a").get("href"),
            "title": show.find("a").get("title")
        } for show in show_details]
        return shows

    def get_show_page(self, q):
        r = requests.get(
            f"{self.base_url}/ajax/v2/tv/seasons/{q.split('-')[-1]}", timeout=10
        ).text
        return r

    def get_show_data(self, q):
        soup = BeautifulSoup(self.get_show_page(q), "html.parser")
        season_data = [(a["data-id"]) for a in soup.find_all("a")]
        episodes = {}
        for i, season in enumerate(season_data):
            r = requests.get(f"{self.base_url}/ajax/v2/season/episodes/{season}").text
            soup = BeautifulSoup(r, "html.parser")
            episodes[f"Season {i + 1}"] = [
                {"id": episode.get("data-id"), "title": episode.get("title")}
                for episode in soup.find_all("a")
            ]
        return episodes

    @staticmethod
    def get_embed_link(provider_links):
        sources = servers(provider_links)
        return sources

    def main(self, q):
        r = requests.get(
            f"{self.base_url}/ajax/v2/episode/servers/{q}/#servers-list"
        ).text
        soup = BeautifulSoup(r, "html.parser")
        show_data = [
            {"id": server.get("data-id"), "server": server.text}
            for server in soup.find_all("a")
        ]
        provider_links = []
        for show in show_data:
            r = requests.get(f"{self.base_url}/ajax/get_link/{show['id']}").text
            provider_links.append(json.loads(r))
        show_sources = self.get_embed_link(provider_links)
        return provider_links, show_sources


class ShowAPI:
    def get_sources(q: str):
        finder = ShowFinder()
        show_choice = finder.get_show_data(q)
        return show_choice

    def get_show_data(q: str):
        finder = ShowFinder()
        show_results = requests.get(f"https://vipstream.tv/search/{q.replace(' ', '-')}", timeout=10).text
        soup = BeautifulSoup(show_results, "html.parser")
        show_details = soup.find_all("div", attrs={"class": "film-detail"})
        show_data = finder.display_shows(show_details)
        shows = []
        for show in show_data:
            if show["id"].startswith("/tv"):
                shows.append(show_info(show["id"], show["title"]))
        return shows

    def get_episodes(q: str):
        finder = ShowFinder()
        show_sources, provider_links = finder.main(q)
        shows = [provider_links, show_sources[0], show_sources[1], show_sources[2]]
        return shows
