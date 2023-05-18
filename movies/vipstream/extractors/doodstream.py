import re

from movies.vipstream.extractors.util.httpclient import HttpClient


class WebScraper:
    def __init__(self):
        self.client = HttpClient()

    def results(self, url):
        req = self.client.get(url).text
        pass_md5 = re.findall(r"/pass_md5/[^']*", req)
        print(pass_md5)


def main(url: str):
    Web = WebScraper()
    Web.results(url)
