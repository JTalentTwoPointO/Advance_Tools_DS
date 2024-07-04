from bs4 import BeautifulSoup
import requests as req
import json
import db


class Scraper:
    def __init__(self):
        self.soup = None
        self.db = db.DB()

    def get(self, url):
        search = f"https://www.reddit.com/search/?q={url}"
        self.soup = BeautifulSoup(req.get(search).text, 'html.parser')

        if self.soup is None:
            print('No soup')
            return []

        for post in self.soup.find_all('faceplate-tracker',
                                       {'data-faceplate-tracking-context': True, "noun": "post", "action": "view"}):
            context = post.get('data-faceplate-tracking-context')

            if context and "post" in context:

                j = json.loads(context)['post']

                if self.db.search_id(j['id']):
                    continue

                self.db.insert(j)
                yield j
