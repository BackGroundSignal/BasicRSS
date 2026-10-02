import requests 
from lxml import etree
from datetime import datetime
from dateutil import parser
import os

class story:
    def __init__(self, feed_name : str = "", story_title : str = "", story_date : str = str(datetime.min), story_url : str = ""):
        self.feed_name = feed_name
        self.story_title = story_title
        self.story_date = parser.parse(story_date)
        self.story_url = story_url

    def get_date_str(self) -> str | None:
        if self.story_date: 
            return self.story_date.strftime("%m/%d/%Y %H:%M:%S")
        else: 
            return None

    def fill_fields_from_xml(self, item : str, feed_name : str) -> None:
        self.feed_name = feed_name
        self.story_title = item.findtext("title")
        self.story_url = item.findtext("link")
        self.story_date = parser.parse(item.findtext("pubDate"))

class feed_reader:
    def __init__(self):
        self.feeds = []
        self.stories = []
    
    def get_feeds_from_txt(self, file_name : str) -> None:
        with open(file_name, "r") as f:
            self.feeds = [line.strip() for line in f.readlines()]
            self.feeds = [line for line in self.feeds if line]

    def grab_stories(self) -> None:
        for feed in self.feeds:
            xml = request_raw_xml(feed)
            if not xml:
                print(f"failed to grab {feed}!")
                continue  
            feed_stories = parse_xml(xml)
            self.stories.extend(feed_stories)
        self.stories = sorted(self.stories, key=lambda x: x.story_date, reverse=True)     
    
    def return_stories(self, num_stories : int) -> list:
        return self.stories[0:max(min(int(num_stories), len(self.stories) - 1), 0)]

def request_raw_xml(url : str) -> str | None:
    res = requests.get(url)
    if res.status_code != 200:
        return None
    return res.content

def parse_xml(xml : str) -> list:
    entries = []
    root = etree.fromstring(xml)
    channel = root.find(".//channel")
    feed_name = channel.findtext("title")
    for item in root.findall(".//item"):
        item_story = story()
        item_story.fill_fields_from_xml(item, feed_name)
        entries.append(item_story)
    return entries

def main() -> None:
    f_reader = feed_reader()
    f_reader.get_feeds_from_txt("feeds.txt")
    print("Grabbing feeds...")
    f_reader.grab_stories()

    num_stories = ""
    while not num_stories.isdigit():
        try:
            num_stories = input("How many stories to grab?: ")
        except Exception as e:
            pass

    returned_stories = f_reader.return_stories(num_stories)

    clear = ""
    while clear.lower() != "y" and clear.lower() != "n":
        try:
            clear = input("Clear the terminal? y/[n]: ") or "y"
        except Exception as e:
            pass
    clear = clear == "y"

    if clear:
        term_clear_str = "cls" if os.name == "nt" else "clear"
        os.system(term_clear_str)

    for s in returned_stories:
        print(f"{s.feed_name} - {s.get_date_str()}\n{s.story_title}\n{s.story_url}\n")
        
if __name__ == "__main__":
    parser.parse(str(datetime.min))
    main()
