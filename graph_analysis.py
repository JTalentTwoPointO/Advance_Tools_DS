import networkx as nx
import matplotlib.pyplot as plt
import igraph as ig
import pandas as pd
from py2neo import Graph

# Function to plot and save NetworkX graph
def plot_networkx_graph(graph, filename, title):
    plt.figure(figsize=(8, 6))
    nx.draw(graph, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray')
    plt.title(title)
    plt.savefig(filename)
    plt.show()

# Function to plot and save igraph graph
def plot_igraph_graph(graph, layout, filename):
    try:
        ig.plot(graph, layout=layout, target=filename, vertex_size=20, vertex_label_size=10, vertex_color='skyblue')
    except ImportError as e:
        print(f"Error plotting igraph: {e}")

# Load CSV data
edges = pd.read_csv('asoiaf-book1-edges.csv')
nodes = pd.read_csv('asoiaf-book1-nodes.csv')

# Print column names to verify
print("Edges columns:", edges.columns)
print("Nodes columns:", nodes.columns)

# Convert node IDs to integers and ensure they are 0-based
nodes['Id'] = nodes['Id'].astype('category').cat.codes
edges['Source'] = edges['Source'].astype('category').cat.codes
edges['Target'] = edges['Target'].astype('category').cat.codes

# Create a NetworkX graph
G_nx = nx.Graph()

# Add nodes
for index, row in nodes.iterrows():
    G_nx.add_node(row['Id'], label=row['Label'])

# Add edges
for index, row in edges.iterrows():
    G_nx.add_edge(row['Source'], row['Target'], weight=row['weight'])  # Adjust column names if necessary

# Plot and save the NetworkX graph
plot_networkx_graph(G_nx, 'asoiaf_network_nx.png', "ASOIAF Network (NetworkX)")

# Create a similar network using igraph
G_ig = ig.Graph.DataFrame(edges[['Source', 'Target', 'weight']], directed=False, vertices=nodes[['Id', 'Label']])
layout = G_ig.layout("kk")
plot_igraph_graph(G_ig, layout, 'asoiaf_network_ig.png')

# Perform analysis on NetworkX graph
pagerank_nx = nx.pagerank(G_nx)
print("PageRank (NetworkX):\n", pagerank_nx)

betweenness_nx = nx.betweenness_centrality(G_nx)
print("Betweenness Centrality (NetworkX):\n", betweenness_nx)

closeness_nx = nx.closeness_centrality(G_nx)
print("Closeness Centrality (NetworkX):\n", closeness_nx)

degree_nx = nx.degree_centrality(G_nx)
print("Degree Centrality (NetworkX):\n", degree_nx)

# Perform analysis on igraph graph
pagerank_ig = G_ig.pagerank()
print("PageRank (igraph):\n", pagerank_ig)

# Load and analyze the Florentine families network (NetworkX)
G_florentine = nx.florentine_families_graph()
plot_networkx_graph(G_florentine, 'florentine_families.png', "Florentine Families Network")

# PageRank (Florentine Families)
pagerank_florentine = nx.pagerank(G_florentine)
print("Florentine Families PageRank:\n", pagerank_florentine)

# Connect to Neo4j and create a graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "Sisma123@"))

# Clear previous data
graph.delete_all()

# Create nodes and relationships in Neo4j
for index, row in nodes.iterrows():
    graph.run("CREATE (n:Character {id: $id, label: $label})", id=row['Id'], label=row['Label'])

for index, row in edges.iterrows():
    graph.run("""
    MATCH (a:Character {id: $source}), (b:Character {id: $target})
    CREATE (a)-[:INTERACTS {weight: $weight}]->(b)
    """, source=row['Source'], target=row['Target'], weight=row['weight'])

# Perform PageRank in Neo4j
pagerank_query = """
CALL gds.pageRank.stream({
  nodeProjection: 'Character',
  relationshipProjection: {
    INTERACTS: {
      type: 'INTERACTS',
      properties: 'weight'
    }
  },
  dampingFactor: 0.85,
  iterations: 20
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).label AS label, score
ORDER BY score DESC
"""
pagerank_results = graph.run(pagerank_query).data()
print("PageRank (Neo4j):", pagerank_results)

# Fetch data from Neo4j and create a NetworkX graph
query = """
MATCH (n)-[r]->(m)
RETURN n, r, m
"""
nodes = {}
G_neo4j = nx.DiGraph()

for record in graph.run(query):
    n = record['n']
    m = record['m']
    r = record['r']

    if n.identity not in nodes:
        nodes[n.identity] = n
        G_neo4j.add_node(n.identity, **n)
    if m.identity not in nodes:
        nodes[m.identity] = m
        G_neo4j.add_node(m.identity, **m)

    G_neo4j.add_edge(n.identity, m.identity, **r)

# Analyze the graph using NetworkX
pagerank_neo4j = nx.pagerank(G_neo4j)
print("PageRank (Neo4j):\n", pagerank_neo4j)