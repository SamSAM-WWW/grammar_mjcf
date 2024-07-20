from create_graphs_with_dag import create_graphs
from DAG import *
from collections import OrderedDict

graph_choose = 1


class Rule():
    def __init__(self):
        self.name = None
        self.lhs_node = None
        self.lhs_edge = None
        self.rhs_node = None
        self.rhs_edge = None
        self.common_node = None
        self.common_edge = None
        self.common_to_lhs_edge_mapping = None
        self.common_to_rhs_edge_mapping = None

def create_rule_from_graph(graph):
    '''
    Rule 类型是一个包含三个子图LHS、RHS、Common的class
    '''
    rule = Rule()
    rule.name = graph.name
    # print("rule_name is",rule.name)

    # Graph must have subgraphs named "L" and "R"
    if not any(graph.lr_subgraph['L'].node_info) or not any(graph.lr_subgraph['R'].node_info):
            raise RuntimeError("Subgraph must contain nodes")


    # Copy nodes into the appropriate graphs in the rule
    l_subgraph_nodes_info = graph.lr_subgraph['L'].node_info
    l_subgraph_edges_info = graph.lr_subgraph['L'].edge_info
    r_subgraph_nodes_info = graph.lr_subgraph['R'].node_info
    r_subgraph_edges_info = graph.lr_subgraph['R'].edge_info
    # print("Nodes in 'L' Subgraph:", l_subgraph_nodes_info)
    # print("Edges in 'L' Subgraph:", l_subgraph_edges_info)
    # print("Nodes in 'R' Subgraph:", r_subgraph_nodes_info)
    # print("Edges in 'R' Subgraph:", r_subgraph_edges_info)



    # Store nodes from 'L' Subgraph in rule's lhs_node
    # rule.lhs_node = list(l_subgraph_nodes_info.items())[0][0]
    # rule.lhs_edge = list(l_subgraph_edges_info.items())
    # rule.rhs_node = list(r_subgraph_nodes_info.items())[1][0]
    # rule.rhs_edge = list(r_subgraph_edges_info.items())
    # Store nodes from 'L' Subgraph in rule's lhs_node, and nodes from 'R' Subgraph in rhs_node
    


    #from LRgraph to Rule of L R Common
    #common nodes and edges
    common_nodes = set(l_subgraph_nodes_info.keys()) & set(r_subgraph_nodes_info.keys())
    common_edges = set(l_subgraph_edges_info.keys()) & set(r_subgraph_edges_info.keys())

    #correct node
    rule.lhs_node = [(name, l_subgraph_nodes_info[name]) for name in l_subgraph_nodes_info]
    rule.rhs_node = [(name, r_subgraph_nodes_info[name]) for name in r_subgraph_nodes_info]
    rule.common_node = sorted([(name, l_subgraph_nodes_info[name]) for name in common_nodes])
    # Convert lists to OrderedDict
    rule.lhs_node = OrderedDict(rule.lhs_node)
    rule.rhs_node = OrderedDict(rule.rhs_node)
    rule.common_node = OrderedDict(rule.common_node)


    #correct edge
    rule.lhs_edge = [(index, l_subgraph_edges_info[index]) for index in l_subgraph_edges_info]
    rule.rhs_edge = [(index, r_subgraph_edges_info[index]) for index in r_subgraph_edges_info]
    rule.common_edge = sorted([(index, l_subgraph_edges_info[index]) for index in common_edges])
    # Convert lists to OrderedDict
    rule.lhs_edge = OrderedDict(rule.lhs_edge)
    rule.rhs_edge = OrderedDict(rule.rhs_edge)
    rule.common_edge = OrderedDict(rule.common_edge)

    # print("rule.lhs_node=",rule.lhs_node)
    # print("rule.lhs_edge=",rule.lhs_edge)
    # print("rule.rhs_node=",rule.rhs_node)
    # print("rule.rhs_edge=",rule.rhs_edge)
    # print("rule.common_node=",rule.common_node)
    # print("rule.common_edge=",rule.common_edge)


    return rule




# graphs = create_graphs(graph_choose)
# for i in range(int(len(graphs))):
#     graph_i = graphs[i]
#     print(f"=================graph{i}====================")
#     create_rule_from_graph(graph_i)