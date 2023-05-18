import re
import json
import requests

from movies.vipstream.util.decrypter import main as decrypter


def get_stream(url):
    provider_link = re.search(r"(https?://[^\s/]+)", url).group(1)
    embed_type, embed_id = re.search(r"embed-(\d+)/(\w+)\??", url).groups()
    r = requests.get(
        f"{provider_link}/ajax/embed-{embed_type}/getSources?id={embed_id}",
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    return json.loads(r.text)


def main(url: str):
    urls = get_stream(url)
    if type(urls["sources"]) == list:
        decrypted_urls = urls["sources"]
    else:
        decrypted_urls = decrypter(urls["sources"])
    sources = {
        "sources": decrypted_urls,
        "tracks": urls["tracks"],
        "server": urls["server"],
    }
    return sources
