import requests 
from lxml import etree
from dateutil import parser
import os

def get_raw_xml(url : str) -> str:
    res = requests.get(url)
    if res.status_code != 200:
        return None
    return res.content

def parse_xml(xml : str) -> dict:
    root = etree.fromstring(xml)
    entries = {}

    channel = root.find(".//channel")
    feed_name = channel.findtext("title")

    for item in root.findall(".//item"):
        title = item.findtext("title")
        url = item.findtext("link")
        date = item.findtext("pubDate")
        if not title or not url:
            continue   
        date_obj = parser.parse(date)
        entries[url] = [title, date_obj, feed_name]
    return entries
    
def main():
    with open("feeds.txt", "r") as f:
        feeds = [line.strip() for line in f.readlines()]
        feeds = [line for line in feeds if line]

    stories = []
    for feed in feeds:
        xml = get_raw_xml(feed)
        if not xml:
            print(f"failed to grab {feed}!")
            continue  
        feed_stories = parse_xml(xml)
        stories.extend(feed_stories.items())

    stories = sorted(stories, key=lambda x: x[1][1], reverse=True)     

    num_stories = ""
    while not num_stories.isdigit():
        try:
            num_stories = input("How many stories to grab?: ")
        except Exception as e:
            pass

    clear_str = "cls" if os.name == "nt" else "clear"
    os.system(clear_str)

    for story in stories[0:int(num_stories)]:
        date_str = story[1][1].strftime("%m/%d/%Y")
        print(f"{story[1][2]} - {date_str}\n{story[1][0]}\n{story[0]}\n")
            

        
if __name__ == "__main__":
    main()