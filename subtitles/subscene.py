from bs4 import BeautifulSoup
from lxml import html 
import requests

root = "https://subscene.com"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
}

async def search_subtitles(q: str):
    r = requests.post(f"{root}/subtitles/searchbytitle", headers=headers, params={"query": q})
    soup = BeautifulSoup(r.content, "html.parser")

    subtitle_links = []
    for a in soup.find_all("a"):
        if a.get("href").startswith("/subtitles/"):
            subtitle_links.append({
                "title": a.text,
                "url": f"{root}{a.get('href')}"
            })

    return subtitle_links


async def download_subtitle(url: str):
    r = requests.get(url, headers=headers)
    objlxml = html.fromstring(r.content)
    btnEl = objlxml.xpath('//*[@id="downloadButton"]')
    return { 
        "link": f"{root}{btnEl[0].get('href')}"
    }
