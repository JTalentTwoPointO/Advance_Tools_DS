import ui, db

if __name__ == '__main__':
    database = db.DB()
    database.clear()  # Clear old data
    ui.MainWindow(database).mainloop()
    # Analyze and save the graph before closing the database
    pagerank_results = database.analyze_graph()
    print("PageRank Results:", pagerank_results)
    database.save_graph("graph.gexf")
    database.close()
