# Reddit Web Scraper & Graph Analyzer

## Overview

This project encompasses a comprehensive analysis of networks using various graph analysis algorithms such as PageRank and HITS. The project includes:
- Web scraping data from Reddit
- Storing and processing the data in a database
- Creating and analyzing graphs using NetworkX and iGraph
- Visualizing graph data and centrality measures
- Integrating with Neo4j for graph database functionalities

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [Graph Analysis and Visualizations](#graph-analysis-and-visualizations)
- [Jupyter Notebook](#jupyter-notebook)

## Features
- **Web Scraping:** Extract data from Reddit using a custom scraper.
- **Database Integration:** Store and manage data using TinyDB and Neo4j.
- **Graph Analysis:** Implement PageRank, HITS, and other centrality measures using NetworkX and iGraph.
- **Visualization:** Visualize graphs and centrality measures with matplotlib and iGraph.
- **UI Interface:** User interface for interacting with the scraper and visualizing data.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/reddit-graph-analyzer.git
   cd reddit-graph-analyzer

2. **Install Required Packages:**
- Ensure you have python 3.7+ installed.
- Create and activate a virtual environment.
   ```bash
      python -m venv env
      source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Setup Neo4j**:
- Install Neo4j:
  - Download and install Neo4j from https://neo4j.com/download-center/#community.
  - Start the Neo4j server.
- Update Credentials:
  - Ensure the Neo4j server is running and accessible at bolt://localhost:7687.
  -Update the credentials in db.py and graph_analysis.py if necessary:
   ```bash
   # Example snippet in db.py and graph_analysis.py
   graph = Graph("bolt://localhost:7687", auth=("neo4j", "your_password"))
   ```
## Usage
- Run The application:
   ```bash
   python main.py
   ```
- **Interact with the UI:**
  - Use the text field to enter a Reddit search term.
  - Click the "Search" button to scrape data.
  - View and analyze the scraped data.

- **Analyze Graph:**
  - Click the "Analyze Graph" button to perform graph analysis.
  - Click the "Visualize Graph" button to view visualizations.

## File Descriptions
- **`asoiaf-book1-nodes.csv` & `asoiaf-book1-edges.csv`**: Data files for creating the graph.
- **`db.py`**: Database interactions with TinyDB and Neo4j.
- **`graph_analysis.py`**: Graph analysis and visualization scripts.
- **`main.py`**: Entry point for the application.
- **`scrape.py`**: Web scraping functionality.
- **`ui.py`**: User interface implementation.
- **`Summaries_of_algorithms.md`**: Detailed explanations of Link Analysis algorithms.
- **`requirements.txt`**: List of required Python packages.

## Graph Analysis and Visualizations
- **Graph Creation**: Create graphs using data from CSV files.
- **Centrality Measures**: Compute PageRank, HITS, Betweenness, Closeness, and Degree centrality.
- **Visualizations**: Save visualizations of graphs and centrality measures in the `graphs` folder.
- **Neo4j Integration**: Interact with a Neo4j database for graph storage and analysis.


## Jupyter Notebook
[graph_analysis.pdf](graph_analysis.pdf)