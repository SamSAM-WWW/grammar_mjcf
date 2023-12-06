from create_graphs_with_dag import create_graphs
from DAG import *
graph_choose = 1


class Rule():
    def __init__(self):
        self.name_ = None
        self.lhs = None
        self.rhs = None
        self.common = None


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
    if not any(graph.lr_subgraph['L'].node_info) or not any(graph.lr_subgraph['R'].node_info):
            raise RuntimeError("Subgraph must contain nodes")


    # Initialize LHS, RHS, and Common subgraphs in the Rule
    rule.lhs = DAG(name="LHS")
    rule.rhs = DAG(name="RHS")
    rule.common = DAG(name="Common")

    # Copy nodes into the appropriate graphs in the rule
    l_subgraph_nodes = list(graph.lr_subgraph['L'].node_info.keys())
    l_subgraph_edges = list(graph.lr_subgraph['L'].edge_info.keys())
    r_subgraph_nodes = list(graph.lr_subgraph['R'].node_info.keys())
    r_subgraph_edges = list(graph.lr_subgraph['R'].edge_info.keys())
    print("Nodes in 'L' Subgraph:", l_subgraph_nodes)
    print("Edges in 'L' Subgraph:", l_subgraph_edges)
    print("Nodes in 'R' Subgraph:", r_subgraph_nodes)
    print("Edges in 'R' Subgraph:", r_subgraph_edges)




    # Continue with the rest of the function...
    print(rule.common.node_info)

    return rule




graphs = create_graphs(graph_choose)

graph_0 = graphs[0]
create_rule_from_graph(graph_0)