import networkx as nx
from tinydb import TinyDB, Query

class DB:
    def __init__(self):
        self.posts = TinyDB("posts.json")
        self.graph = nx.Graph()

    def insert(self, data):
        self.posts.insert(data)
        self.graph.add_node(data['id'], label=data['title'])
        # Add an edge (adjust according to our requirements)
        if 'related_id' in data:
            self.graph.add_edge(data['id'], data['related_id'])

    def search_id(self, id):
        return self.posts.search(Query().id == id)

    def close(self):
        self.posts.close()

    def get_all(self):
        return self.posts.all()

    def analyze_graph(self):
        # Implemented PageRank analysis
        return nx.pagerank(self.graph)

    def save_graph(self, filename):
        nx.write_gexf(self.graph, filename)

    def load_graph(self, filename):
        self.graph = nx.read_gexf(filename)

    def clear(self):
        self.posts.truncate()
        self.graph.clear()