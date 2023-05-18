import re
import requests
from bs4 import BeautifulSoup

def get_description(soup):
    element_div = soup.find("div", {"class": "description"})
    description = element_div.text.strip()
    return description

def get_duration(soup):
    elements_div = soup.find_all('div', {"class": "row-line"})
    elements = [element.text.strip() for element in elements_div]
    duration_str = [e for e in elements if "Duration" in e][0].replace("Duration:", "").strip()
    duration = duration_str.split(" ")[0]
    return duration 
        
def get_release_date(soup):
    elements_div = soup.find_all('div', {"class": "row-line"})
    elements = [element.text.strip() for element in elements_div]
    return elements[0].replace("Released:  ", "") 

def get_casts(soup):
    elements_div = soup.find_all('div', {"class": "row-line"})
    elements = [element.text.strip() for element in elements_div]
    elements = [e for e in elements if "Duration" not in e]
    elements = [e.strip() for e in elements]
    casts = [c.strip() for c in elements[2].replace('Casts:', '').split(',')]
    return casts

def get_country(soup):
    elements_div = soup.find_all('div', {"class": "row-line"})
    elements = [element.text.strip() for element in elements_div]
    elements = [e for e in elements if "Duration" not in e]
    elements = [e.strip() for e in elements]
    country_string = elements[3:][0].replace("\n", "").replace("Country: ", "").strip()
    country_list = re.split(r'\s{2,}', country_string)
    country_names = ' '.join(country_list)
    return country_names


def get_image(soup):
    image = soup.find('img', {'class': 'film-poster-img'})
    return image['src']

def main(id, title):
    r = requests.get(f"https://vipstream.tv/{id}").text
    soup = BeautifulSoup(r, "html.parser")

    image = get_image(soup)
    description = get_description(soup)
    release_date = get_release_date(soup)
    casts = get_casts(soup)
    duration = get_duration(soup)
    country = get_country(soup)

    show_data = {
        "image": image, 
        "title": title,
        "description": description,
        "id": id,
        "release-date": release_date,
        "casts": casts,
        "duration": duration,
        "country": country
    }
    return show_data
