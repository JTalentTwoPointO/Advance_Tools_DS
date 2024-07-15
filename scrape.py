from bs4 import BeautifulSoup
import requests as req
import json
import db


class Scraper:
    def __init__(self, database):
        print("Initializing Scraper")
        self.soup = None
        self.db = database

    def get(self, url):
        try:
            print(f"Fetching URL: {url}")
            search = f"https://www.reddit.com/search/?q={url}"
            response = req.get(search)
            response.raise_for_status()  # Raises an error for bad response
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

                    print(f"Inserting post: {j['title']}")  # Debug statement
                    self.db.insert(j)
                    yield j
        except req.RequestException as e:
            print(f"Error fetching url: {e}")
