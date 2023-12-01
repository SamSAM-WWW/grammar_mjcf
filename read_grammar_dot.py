import networkx as nx
import os
import pygraphviz as pgv
import pydot
import re
from networkx.drawing.nx_pydot import read_dot
current_dir = os.getcwd()
grammar_dir = "grammar_data"
file_dir = "grammar_apr30.dot"


def parse_dot(input_data):
    # 提取有关图形的信息
    graphs = []
    current_subgraph = None
    graph_pattern = re.compile(r'(?:digraph|subgraph) (\w+) \{([\s\S]*?)\}')
    
    for match in graph_pattern.finditer(input_data):
        name = match.group(1)
        body = match.group(2)
        
        # 如果是子图，则更新当前子图的名称
        if name.startswith("subgraph "):
            current_subgraph = name.split()[1]
            continue

        nodes = re.findall(r'(\w+)\s*\[.*?\];', body)
        edges = re.findall(r'(\w+)\s*->\s*(\w+)\s*\[.*?\];', body)
        graphs.append((name, current_subgraph, nodes, edges))

    return graphs

def load_graphs(path):
    nx_graphs = []

    # Read the DOT file into a list of NetworkX graphs
    dot_graphs = read_dot(path)

    # Process each graph
    for i, dot_graph in enumerate(dot_graphs):
        print(f"Processing graph {i + 1}")

        nx_graph = nx.Graph()
        
        # Extract nodes and edges
        nodes = list(dot_graph.nodes)
        edges = list(dot_graph.edges)

        print(f"Nodes: {nodes}")
        print(f"Edges: {edges}")

        # Check if the graph has a 'subgraph' attribute
        subgraph_attr = dot_graph.graph.get('subgraph')
        if subgraph_attr:
            nx_graph.graph['subgraph'] = subgraph_attr

        # Add nodes and edges to the NetworkX graph
        nx_graph.add_nodes_from(nodes)
        nx_graph.add_edges_from(edges)

        nx_graphs.append(nx_graph)

    return nx_graphs
# def load_graphs(path):
#     graphs = []
    
#     # Assuming the file contains graph data in DOT language
#     with open(path, 'r') as file:
#         file_content = file.read()
#         # Use pygraphviz to read the entire DOT file
#         all_graphs = pgv.AGraph(file_content)
        
#         # Iterate over subgraphs
#         for subgraph in all_graphs.subgraphs():
#             # Convert each subgraph to a NetworkX graph
#             nx_graph = nx.drawing.nx_agraph.from_agraph(subgraph)
#             graphs.append(nx_graph)

#     return graphs


class Rule():
    def __init__(self):
        self.name = None
        self.lhs = None
        self.rhs = None
        self.common = None
        self.common_to_lhs = None
        self.common_to_rhs = None

def create_rule_from_graph(graph):
    '''
    Rule 类型是一个包含三个子图LHS、RHS、Common的class

    struct Rule {
    `name`
    
    Left-Hand Side (LHS) subgraph
    `Graph lhs_;`

    Right-Hand Side (RHS) subgraph
    `Graph rhs_;`

    Common subgraph
    `Graph common_;`
    };
    '''
    rule = Rule()
    rule.name = graph.name
    print("rule_name is",rule.name)

    # Graph must have subgraphs named "L" and "R"
    # subgraph_ = graph.subgraph()
    # subgraph_name = subgraph_.name






    # Continue with the rest of the function...

    return rule













# test
grammar_path = os.path.join(current_dir, grammar_dir, file_dir )

graphs = load_graphs(grammar_path)
print(graphs)
print(f"Number of graphs loaded: {len(graphs)}")

# Print detailed information about each graph
for i, graph in enumerate(graphs):
    print(f"\nGraph {i + 1} Info:")
    print(nx.info(graph))
    print("Nodes:", graph.nodes())
    print("Edges:", graph.edges())
    print("Attributes:", graph.graph)

rules = [create_rule_from_graph(g) for g in graphs]