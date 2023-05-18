from bs4 import BeautifulSoup
from fastapi import FastAPI 
from lxml import html 
import requests

app = FastAPI()
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
                "id": a.get("href")
            })

    return subtitle_links


async def parse_url(sub_id: str):
    sub_page = requests.get(root + sub_id, headers=headers)
    soup = BeautifulSoup(sub_page.content, "html.parser")
    sub_links = []
    for link in soup.find_all("a"):
        if link.get("href").startswith("/subtitles/"):
            sub_links.append({
                "link": root + link.get('href')
            })
    return sub_links


async def sub_file(sub_url: str):
    r = requests.get(sub_url, headers=headers)
    objlxml = html.fromstring(r.content)
    btnEl = objlxml.xpath('//*[@id="downloadButton"]')
    return { 
        "link": root + btnEl[0].get("href")
    }
