import requests 
import random
from lxml import etree

def get_raw_xml(url : str) -> str:
    res = requests.get(url)
    if res.status_code != 200:
        return None
    return res.content


def main():
    urls = ["https://www.propublica.org/feeds/propublica/main", "https://www.404media.co/rss/", "https://feedx.net/rss/ap.xml", "https://feeds.feedburner.com/motherjones/feed"]
    xml = get_raw_xml(random.choice(urls))
    if not xml:
        print("failed to grab!")
        return None  

if __name__ == "__main__":
    main()