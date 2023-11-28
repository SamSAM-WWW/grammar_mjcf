import networkx as nx
import os
import pygraphviz as pgv
current_dir = os.getcwd()
grammar_dir = "grammar_data"
file_dir = "grammar_apr30.dot"



def load_graphs(path):
    graphs = []

    # Assuming the file contains graph data in DOT language
    with open(path, 'r') as file:
        file_content = file.read()
        # Use pygraphviz to read the entire DOT file
        full_graph = pgv.AGraph(file_content)
        
        # Iterate over subgraphs
        for subgraph in full_graph.subgraphs():
            # Convert each subgraph to a NetworkX graph
            nx_graph = nx.drawing.nx_agraph.from_agraph(subgraph)
            graphs.append(nx_graph)

    return graphs


# test
# grammar_path = os.path.join(current_dir, grammar_dir, file_dir )

# graphs = load_graphs(grammar_path)
# print(graphs)
# print(f"Number of graphs loaded: {len(graphs)}")

# # Print detailed information about each graph
# for i, graph in enumerate(graphs):
#     print(f"\nGraph {i + 1} Info:")
#     print(nx.info(graph))