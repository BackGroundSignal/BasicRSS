import requests 
import random
from lxml import etree

def get_raw_xml(url : str) -> str:
    res = requests.get(url)
    if res.status_code != 200:
        return None
    return res.content

def parse_xml(xml : str) -> dict:
    root = etree.fromstring(xml)
    entries = {}
    for item in root.findall(".//item"):
        title = item.findtext("title")
        url = item.findtext("link")
        if not title or not url:
            continue        
        entries[title] = url
    # TODO: get content / description?
    return entries
    
def main():
    with open("feeds.txt", "r") as f:
        feeds = [line.strip() for line in f.readlines()]

    for feed in feeds:
        xml = get_raw_xml(feed)
        if not xml:
            print("failed to grab!")
            return None  
        
        stories = parse_xml(xml)
        for item in stories:
            print(f"{item}\n{stories[item]}\n")
        
        print("\n")

if __name__ == "__main__":
    main()