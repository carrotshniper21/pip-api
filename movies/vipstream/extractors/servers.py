from movies.vipstream.extractors.rabbitstream import main as rabbitstream
from movies.vipstream.extractors.streamlare import main as streamlare
from movies.vipstream.extractors.dokicloud import main as dokicloud
from movies.vipstream.util.mvbasemodel import main as basemodel


def contains_link(link):
    return ("dokicloud" in link) or ("rabbitstream" in link) or ("streamlare" in link)

def main(data):
    doki_links = []
    rabbit_links = []
    streamlare_links = []

    for i, dictionary in enumerate(data):
        link = dictionary["link"]
        if contains_link(link):
            if i == 0:
                doki_links = dokicloud(f"{link}")
            elif i == 1:
                rabbit_links = rabbitstream(f"{link}")
            elif i == 2:
                streamlare_links = streamlare(f"{link}")
        else:
            pass

    dl, rl, sl = basemodel(doki_links, rabbit_links, streamlare_links)
    return (dl.dict(), rl.dict(), sl.dict())


