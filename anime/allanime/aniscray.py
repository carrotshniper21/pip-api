import json
import requests
from typing import List, Tuple, Optional
from anime.allanime import anime_info

class AnimeScraper:

    def __init__(self):
        self.base_url = "https://allanime.to"
        self.api_url = "https://api.allanime.to/allanimeapi"
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; rv:109.0) Gecko/20100101 Firefox/109.0"
        self.headers = {
            "User-Agent": self.user_agent,
            "Referer": self.base_url,
        }

    def search_anime(self, query: str) -> List[Tuple[str, str]]:
        search_gql = """
        query(
            $search: SearchInput
            $limit: Int
            $page: Int
            $translationType: VaildTranslationTypeEnumType
            $countryOrigin: VaildCountryOriginEnumType
        ) {
            shows(
                search: $search
                limit: $limit
                page: $page
                translationType: $translationType
                countryOrigin: $countryOrigin
            ) {
                edges {
                    _id name availableEpisodes __typename
                }
            }
        }
        """
        variables = {
            "search": {"allowAdult": False, "allowUnknown": False, "query": query},
            "limit": 40,
            "page": 1,
            "translationType": "sub",
            "countryOrigin": "ALL",
        }
        response = requests.get(
            self.api_url,
            headers=self.headers,
            params={"query": search_gql, "variables": json.dumps(variables)},
        )
        data = response.json()
        anime_list = []

        for edge in data["data"]["shows"]["edges"]:
            anime_list.append(anime_info.main(edge["_id"]))

        return anime_list

    def get_episodes(self, anime_id: str) -> List[str]:
        episodes_list_gql = """
        query ($showId: String!) {
            show(
                _id: $showId
            ) {
                _id availableEpisodesDetail
            }
        }
        """
        variables = {"showId": anime_id}
        response = requests.get(
            self.api_url,
            headers=self.headers,
            params={"query": episodes_list_gql, "variables": json.dumps(variables)},
        )
        data = response.json()
        episodes = data["data"]["show"]["availableEpisodesDetail"]

        return episodes

    def get_episode_url(self, anime_id: str, episode: str) -> Optional[str]:
        episode_embed_gql = """
        query ($showId: String!, $translationType: VaildTranslationTypeEnumType!, $episodeString: String!) {
            episode(
                showId: $showId
                translationType: $translationType
                episodeString: $episodeString
            ) {
                episodeString sourceUrls
            }
        }
        """
        variables = {
            "showId": anime_id,
            "translationType": "sub",
            "episodeString": episode,
        }
        response = requests.get(
            self.api_url,
            headers=self.headers,
            params={"query": episode_embed_gql, "variables": json.dumps(variables)},
        )
        data = response.json()

        if "data" not in data or "episode" not in data["data"]:
            print("Error: Unexpected data format.")
            return None

        source_urls = data["data"]["episode"]["sourceUrls"]

        return source_urls

    def download_episode(self, url: str, filename: str) -> None:
        response = requests.get(url, headers=self.headers, stream=True)

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
