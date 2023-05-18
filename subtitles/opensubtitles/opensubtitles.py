from bs4 import BeautifulSoup
from lxml import html
import requests

root = "https://www.opensubtitles.org"

async def get_xml_data(lang_code: str, media_name: str):
    xml_data = requests.get(f"{root}/en/search/sublanguageid-{lang_code}/moviename-{media_name}/atom_1_00.xml").text
    soup = BeautifulSoup(xml_data, "xml")

    subtitle_links = []
    for i, entry in enumerate(soup.find_all("entry")):
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

async def parse_url(q: str):
    response = requests.get(q)
    objlxml = html.fromstring(response.content)
    btnEl = objlxml.xpath("//a[@id='bt-dwl-bt']")

    if len(btnEl):
        downloadUrl = root + btnEl[0].get("href")
        return {
            "download_link": downloadUrl
        }
