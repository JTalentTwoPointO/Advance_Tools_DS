from tinydb import TinyDB, Query

class DB:
    def __init__(self):
        self.posts = TinyDB("posts.json")

    def insert(self, data):
        self.posts.insert(data)

    def search_id(self, id):
        return self.posts.search(Query().id == id)

    def close(self):
        self.posts.close()

    def get_all(self):
        return self.posts.all()