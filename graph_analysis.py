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
    plt.savefig(filename)
    plt.show()


def plot_igraph_graph(graph, layout, filename):
    try:
        ig.plot(graph, layout=layout, target=filename, vertex_size=20, vertex_label_size=10, vertex_color='skyblue')
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

    betweenness_nx = nx.betweenness_centrality(G_nx)
    print("Betweenness Centrality (NetworkX):\n", betweenness_nx)

    closeness_nx = nx.closeness_centrality(G_nx)
    print("Closeness Centrality (NetworkX):\n", closeness_nx)

    degree_nx = nx.degree_centrality(G_nx)
    print("Degree Centrality (NetworkX):\n", degree_nx)

    pagerank_ig = G_ig.pagerank()
    print("PageRank (igraph):\n", pagerank_ig)

    G_florentine = nx.florentine_families_graph()
    plot_networkx_graph(G_florentine, 'florentine_families.png', "Florentine Families Network")

    pagerank_florentine = nx.pagerank(G_florentine)
    print("Florentine Families PageRank:\n", pagerank_florentine)

    graph = Graph("bolt://localhost:7687", auth=("neo4j", "Sisma123"))
    graph.delete_all()

    for index, row in nodes.iterrows():
        graph.run("CREATE (n:Character {id: $id, label: $label})", id=row['Id'], label=row['Label'])

    for index, row in edges.iterrows():
        graph.run("""
        MATCH (a:Character {id: $source}), (b:Character {id: $target})
        CREATE (a)-[:INTERACTS {weight: $weight}]->(b)
        """, source=row['Source'], target=row['Target'], weight=row['weight'])

    # Perform PageRank in Neo4j
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
