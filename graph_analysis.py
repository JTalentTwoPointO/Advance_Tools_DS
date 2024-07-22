import os
import networkx as nx
import matplotlib.pyplot as plt
import igraph as ig
import pandas as pd
from py2neo import Graph

# Define global variables
G_nx = None
G_florentine = None


def plot_networkx_graph(graph, filename, title):
    plt.figure(figsize=(8, 6))
    nx.draw(graph, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray')
    plt.title(title)
    plt.savefig(os.path.join('graphs', filename))
    plt.close()

def plot_centrality_measures(measure, title, filename):
    plt.figure(figsize=(10, 6))
    nodes = list(measure.keys())
    values = list(measure.values())
    plt.bar(nodes, values, color='skyblue')
    plt.xlabel('Nodes')
    plt.ylabel('Centrality Value')
    plt.title(title)
    plt.legend(['Centrality Measure'])
    plt.savefig(os.path.join('graphs', filename))
    plt.close()

def plot_igraph_graph(graph, layout, filename):
    try:
        ig.plot(graph, layout=layout, target=os.path.join('graphs', filename), vertex_size=20, vertex_label_size=10, vertex_color='skyblue')
    except ImportError as e:
        print(f"Error plotting igraph: {e}")

def analyze_graph():
    global G_nx, G_florentine

    edges = pd.read_csv('asoiaf-book1-edges.csv')
    nodes = pd.read_csv('asoiaf-book1-nodes.csv')

    nodes['Id'] = nodes['Id'].astype('category').cat.codes
    edges['Source'] = edges['Source'].astype('category').cat.codes
    edges['Target'] = edges['Target'].astype('category').cat.codes

    G_nx = nx.Graph()
    for index, row in nodes.iterrows():
        G_nx.add_node(row['Id'], label=row['Label'])

    for index, row in edges.iterrows():
        G_nx.add_edge(row['Source'], row['Target'], weight=row['weight'])

    plot_networkx_graph(G_nx, 'asoiaf_network_nx.png', "ASOIAF Network (NetworkX)")

    G_ig = ig.Graph.DataFrame(edges[['Source', 'Target', 'weight']], directed=False, vertices=nodes[['Id', 'Label']])
    layout = G_ig.layout("kk")
    plot_igraph_graph(G_ig, layout, 'asoiaf_network_ig.png')

    pagerank_nx = nx.pagerank(G_nx)
    print("PageRank (NetworkX):\n", pagerank_nx)
    plot_centrality_measures(pagerank_nx, "PageRank (NetworkX)", "pagerank_nx.png")

    betweenness_nx = nx.betweenness_centrality(G_nx)
    print("Betweenness Centrality (NetworkX):\n", betweenness_nx)
    plot_centrality_measures(betweenness_nx, "Betweenness Centrality (NetworkX)", "betweenness_nx.png")

    closeness_nx = nx.closeness_centrality(G_nx)
    print("Closeness Centrality (NetworkX):\n", closeness_nx)
    plot_centrality_measures(closeness_nx, "Closeness Centrality (NetworkX)", "closeness_nx.png")

    degree_nx = nx.degree_centrality(G_nx)
    print("Degree Centrality (NetworkX):\n", degree_nx)
    plot_centrality_measures(degree_nx, "Degree Centrality (NetworkX)", "degree_nx.png")

    pagerank_ig = G_ig.pagerank()
    print("PageRank (igraph):\n", pagerank_ig)
    plot_centrality_measures(dict(enumerate(pagerank_ig)), "PageRank (igraph)", "pagerank_ig.png")

    G_florentine = nx.florentine_families_graph()
    plot_networkx_graph(G_florentine, 'florentine_families.png', "Florentine Families Network")

    pagerank_florentine = nx.pagerank(G_florentine)
    print("Florentine Families PageRank:\n", pagerank_florentine)
    plot_centrality_measures(pagerank_florentine, "Florentine Families PageRank", "pagerank_florentine.png")

    graph = Graph("bolt://localhost:7687", auth=("neo4j", "Sisma123"))
    graph.delete_all()

    for index, row in nodes.iterrows():
        graph.run("CREATE (n:Character {id: $id, label: $label})", id=row['Id'], label=row['Label'])

    for index, row in edges.iterrows():
        graph.run("""
        MATCH (a:Character {id: $source}), (b:Character {id: $target})
        CREATE (a)-[:INTERACTS {weight: $weight}]->(b)
        """, source=row['Source'], target=row['Target'], weight=row['weight'])

    pagerank_query = """
        CALL gds.pageRank.stream('characterGraph', {
        dampingFactor: 0.85,
        maxIterations: 20
        })
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).label AS label, score
        ORDER BY score DESC
    """

    pagerank_results = graph.run(pagerank_query).data()
    print("PageRank (Neo4j):", pagerank_results)

    query = """
    MATCH (n:Character)-[r:INTERACTS]->(m:Character)
    RETURN n, r, m
    """
    nodes_dict = {}
    G_neo4j = nx.DiGraph()

    for record in graph.run(query):
        n = record['n']
        m = record['m']
        r = record['r']

        if n['id'] not in nodes_dict:
            nodes_dict[n['id']] = n
            G_neo4j.add_node(n['id'], label=n['label'])
        if m['id'] not in nodes_dict:
            nodes_dict[m['id']] = m
            G_neo4j.add_node(m['id'], label=m['label'])

        G_neo4j.add_edge(n['id'], m['id'], weight=r['weight'])

    pagerank_neo4j = nx.pagerank(G_neo4j)
    print("PageRank (Neo4j):\n", pagerank_neo4j)
    plot_centrality_measures(pagerank_neo4j, "PageRank (Neo4j)", "pagerank_neo4j.png")
