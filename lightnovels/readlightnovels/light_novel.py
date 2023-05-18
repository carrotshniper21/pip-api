from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

"""
novel_results = novel_searcher(q.replace(" ", "+"))
novel_attrs = novel_info(novel_results)
novel_chapters = novel_chapter_chooser(novel_results)
novel_chapter_text = get_chapter_text(novel_chapters)
"""

app = FastAPI()
root = "https://readlightnovels.net"

async def novel_searcher(q):
    novel_results = requests.get(f"{root}?s={q.replace(' ', '+')}").text
    soup = BeautifulSoup(novel_results, "html.parser")
    novel_info = soup.find_all(
        "div", {"class": "col-md-3 col-sm-6 col-xs-6 home-truyendecu"}
    )
  
    novel_responses = []
    for novel in novel_info:
        novel_href = novel.find("a")["href"]
        novel_img = novel.find("img")
        novel_img_src = novel_img["src"]
        novel_img_alt = novel_img["alt"]
        novel_responses.append({
            "href": novel_href, "image": novel_img_src, "title": novel_img_alt
        })
    return novel_responses
  
  
async def novel_info(novel_link: str):
    novel_info = []
    novel_response = requests.get(novel_link).text
    soup = BeautifulSoup(novel_response, "html.parser")
    novel_desc = soup.find_all("div", {"class": "col-xs-12 col-info-desc"})
    for desc in novel_desc:
        description = desc.find("div", {"class": "desc-text"})
        info = desc.find("div", {"class": "info"}).text.split("\n")
        info = [i.split(":") for i in info if i]
        novel_info.append({
            "author": info[0][1],
            "genres": info[1][1],
            "status": info[2][1],
            "views": info[3][1],
            "description": description.text
        })
    return novel_info
  
  
async def novel_chapter_chooser(novel_link: str):
    novel_chapters = []
    novel_response = requests.get(novel_link).text
    soup = BeautifulSoup(novel_response, "html.parser")
    chapter_list = soup.find("div", {"class": "col-xs-12 col-sm-6 col-md-6"})
    chapter_ul = chapter_list.find("ul")
    for a_tag in chapter_ul.find_all("a"):
        novel_chapters.append({
            "href": a_tag.get("href"),
            "title": a_tag.get("title"),
        })
    return novel_chapters
  
  
async def get_chapter_text(chapter_link: str):
    chapter_text = []
    chapter_response = requests.get(chapter_link).text
    soup = BeautifulSoup(chapter_response, "html.parser")
    chapter_text.append({
        "chapter_text": soup.find("div", {"class": "chapter-content"}).text
    })
    return chapter_text
