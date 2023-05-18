import re
import json

import requests
from bs4 import BeautifulSoup

def get_csrf_token(server_url: str):
    r = requests.get("https://sltube.org/e/{server_url}").text
    soup = BeautifulSoup(r, "html.parser")
    try:
        csrf_token = soup.find("meta", {"name": "csrf-token"}).get("content")
    except AttributeError:
        return None
    return csrf_token

def get_stream(server_url):
    server_id = re.search(r"/([^/]+)$", server_url).group(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Referer": f"https://sltube.org/e/{server_id}",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRF-TOKEN": get_csrf_token(server_id),
        "Content-Type": "application/json;charset=utf-8",
    }
    response = requests.post(
        "https://sltube.org/api/video/stream/get", headers=headers, data=f'{{"id":"{server_id}"}}'
    )
    return json.loads(response.content)


def main(server_url: str):
    urls = get_stream(server_url)
    return urls
