from bs4 import BeautifulSoup
from lxml import html
import requests

root = "https://www.opensubtitles.org"

async def search_subtitles(q: str):
    xml_data = requests.get(f"{root}/en/search/sublanguageid-all/moviename-{q}/atom_1_00.xml").content
    soup = BeautifulSoup(xml_data, "xml")

    subtitle_links = []
    for _, entry in enumerate(soup.find_all("entry")):
        title = entry.find("title").text
        link = entry.find("link").get("href")
        updated = entry.find("updated").text
        summary = entry.find("summary").text
        subtitle_links.append({
            "link": link,
            "title": title, 
            "updated": updated, 
            "info": summary
        })

    return subtitle_links

async def download_subtitle(url: str):
    response = requests.get(url)
    objlxml = html.fromstring(response.content)
    btnEl = objlxml.xpath("//a[@id='bt-dwl-bt']")

    if len(btnEl):
        downloadUrl = root + btnEl[0].get("href")
        return {
            "download_link": downloadUrl
        }
