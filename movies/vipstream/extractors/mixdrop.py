import re
import json

import requests
from bs4 import BeautifulSoup


def get_stream(server_url):
    server_id = re.search(r"/([^/]+)$", server_url).group(1)
    csrf_token = lambda server_url: str(
        BeautifulSoup(
            requests.get(f"https://sltube.org/e/{server_url}").text, "html.parser"
        )
        .find("meta", {"name": "csrf-token"})
        .get("content")
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Referer": f"https://sltube.org/e/{server_id}",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRF-TOKEN": csrf_token(server_id),
        "Content-Type": "application/json;charset=utf-8",
    }
    data = f'{{"id":"{server_id}"}}'

    response = requests.post(
        "https://sltube.org/api/video/stream/get", headers=headers, data=data
    )
    return json.loads(response.content)


def main(server_url: str):
    urls = get_stream(server_url)
    return urls


if __name__ == "__main__":
    main()
