import networkx as nx
import argparse
import ast
import csv
import datetime
import numpy as np
import os
import random
import signal
import sys
from RobotGraph import RobotGraph

def make_initial_graph():
    G = nx.DiGraph(name = 'arobot')
    G.add_node('robot',label ='robot')
    # print(G.nodes.data())
    return G


def apply_rule(rule,target_graph:RobotGraph ,lhs_to_target,target_node_name):
    '''
    功能:对机器人图进行操作，使用规则后得到新的机器人图
    ---------------
    输入:选定的一个规则；待修改的机器人图（类型为RobotGraph）；待修改的节点

    输出:修改后的机器人图（类型为RobotGraph）
    '''
    # Copy target nodes not in LHS to result
    # print("trying to apply rule 1 Copy target nodes not in LHS to result")
    result_graph = target_graph.copy()
    lhs_nodes = set(rule.lhs_node.keys())
    # print("lhs_nodes = ",lhs_nodes)
        # 遍历目标图的节点
    for node in target_graph.nodes(data=True):
        node_name, node_data = node
        # print("target_graph.nodes node_name, node_data = ",node_name, node_data)
        # 如果节点不在LHS中，将其复制到结果图中
        if node_name not in lhs_nodes and node_name != 'parent' and node_name != 'child':
            # print("apply rule 1 Copy target nodes not in LHS to result",node_name)
            result_graph.add_node(node_name, **node_data)

    # Copy target nodes in LHS to result if they are in common with the RHS
    common_nodes = set(rule.common_node.keys())
    # print("common_nodes = ", common_nodes)
    # print("trying to apply rule 2 Copy target nodes in LHS to result if they are in common with the RHS")
    for lhs_node_name in rule.lhs_node.keys():
        # Check if the corresponding RHS node is in the target graph and in common with the LHS
        if lhs_node_name in common_nodes and lhs_node_name in target_graph.nodes() and node_name != 'parent' and node_name != 'child':
            # Copy the common node to the result graph
            # print("apply rule 2 Copy target nodes in LHS to result if they are in common with the RHS", lhs_node_name)
            result_graph.add_node(lhs_node_name, **target_graph.nodes[lhs_node_name])
    
    # Add RHS nodes which are not in common with the LHS
    rhs_node_info = rule.rhs_node
    # print("trying to apply rule 3 Add RHS nodes which are not in common with the LHS")
    for node_name, node_attrs in rhs_node_info.items():
        if node_name not in lhs_to_target['node_mapping'].values() and node_name != 'parent' and node_name != 'child':
            # print("apply rule 3 Add RHS nodes which are not in common with the LHS",node_name)
            result_graph.add_node(node_name, **node_attrs)  



    # Copy target edges not in LHS to result
        # lhs_edges = set(rule.lhs_edge)wrong
    lhs_edges = set((src, dest) for src, dest_info in rule.lhs_edge.items() for dest, _ in dest_info.items())
    lhs_edges_with_parent = set({(src, dest) for src, dest_info in rule.lhs_edge.items() for dest, _ in dest_info.items() if "parent" in src})
    lhs_edges_with_child = set({(src, dest) for src, dest_info in rule.lhs_edge.items() for dest, _ in dest_info.items() if "child" in dest})
    common_lhs_edges = lhs_edges - lhs_edges_with_parent - lhs_edges_with_child


    # print("trying to apply rule 4 Copy target edges not in LHS to result")
    for edge in target_graph.edges():
        edge_start, edge_end = edge
        # print(edge,edge_start,edge_end)

        if (edge_start, edge_end) not in common_lhs_edges:
            # print("apply rule 4 Copy target edges not in LHS to result",edge_start,edge_end)
            result_graph.add_edge(edge_start, edge_end, **target_graph.edges[edge])
        
        if any(edge_end == dest for _, dest in lhs_edges_with_parent):
            # print("apply rule 4 Copy target edges not in LHS to result")
            result_graph.add_edge(edge_start, edge_end, **target_graph.edges[edge])
        
        if any(edge_start == src for src, _ in lhs_edges_with_child):
            # print("apply rule 4 Copy target edges not in LHS to result")
            result_graph.add_edge(edge_start, edge_end, **target_graph.edges[edge])


    # Copy target edges in LHS to result if they are in common with the RHS
    common_edges = set((src, dest) for src, dest_info in rule.common_edge.items() for dest, _ in dest_info.items())
    common_edges_with_parent = set({(src, dest) for src, dest_info in rule.common_edge.items() for dest, _ in dest_info.items() if "parent" in src})
    common_edges_with_child = set({(src, dest) for src, dest_info in rule.common_edge.items() for dest, _ in dest_info.items() if "child" in dest})
    common_edges_without_parent_child = common_edges - common_edges_with_parent - common_edges_with_child

    # print("rule.lhs_edge = ",rule.lhs_edge)
    # lhs_edges = set(rule.lhs_edge)
    lhs_edges = set((src, dest) for src, dest_info in rule.lhs_edge.items() for dest, _ in dest_info.items())
    lhs_edges_with_parent = set({(src, dest) for src, dest_info in rule.lhs_edge.items() for dest, _ in dest_info.items() if "parent" in src})
    lhs_edges_with_child = set({(src, dest) for src, dest_info in rule.lhs_edge.items() for dest, _ in dest_info.items() if "child" in dest})
    common_lhs_edges = lhs_edges - lhs_edges_with_parent - lhs_edges_with_child

    # print("trying to apply rule 5 Copy target edges not in LHS to result")
    # print("lhs_edges = ",lhs_edges)

    for lhs_edge in lhs_edges:
        if lhs_edge in target_graph.edges() and lhs_edge in common_edges:
            # print("apply rule 5 Copy target edges not in LHS to result", lhs_edge)
            result_graph.add_edge(lhs_edge[0], lhs_edge[1], **target_graph.edges[lhs_edge])

    # Add RHS edges which are not in common with the LHS
    rhs_edges = rule.rhs_edge.items()
    # ("trying to apply rule 6 Add RHS edges which are not in common with the LHS")
    for start_node, edge_data in rhs_edges:
        for end_node, attributes in edge_data.items():
            # Now 'start_node', 'end_node', and 'attributes' hold the necessary information
            # 'attributes' is a dictionary containing edge attributes
            rhs_edge = (start_node, end_node, attributes)
            result_graph.add_edge(start_node, end_node, **attributes)
    return result_graph


def find_matches(rule,graph):
    matches = []
    # 遍历图中的节点
    for node in graph.nodes(data=True):
        # print("finding matches")
        node_name, node_data = node
        # print("finding matches, graph node name = ", node_name)
        # print("finding matches, graph node data = ", node_data)

        # 检查节点是否匹配规则的左侧
        # print ("find_matches rule.lhs_node = ",rule.lhs_node)
        if node_name in rule.lhs_node:
            lhs_mapping = rule.lhs_node[node_name]
            match = {'node_mapping': {tuple(lhs_mapping.items()): node_name}}
            # print("Debug: Initial match:", match)
            matches.append(match)
            # print("Debug: Initial matches:", matches)
    
    # print("return matches = ", matches)
    return matches


def check_rule_applicability(rule, target_graph, match):
    # LHS中存在但与RHS不共有的目标节点将被移除
    target_nodes_to_remove = []

    for node_name, node_data in target_graph.nodes(data=True):
        if node_name in rule.lhs_node and node_name not in rule.common_node:
            target_nodes_to_remove.append(node_name)
    # print("target_graph.nodes = ",target_graph.nodes)
    # print("target_nodes_to_remove = ",target_nodes_to_remove)
    # 检查不在LHS中的目标边是否与将要移除的节点相邻（悬空条件）
    for target_edge in target_graph.edges:
        # print("target_edge = ",target_edge)
        if target_edge not in rule.lhs_edge:
            source, target = target_edge
            # print("source = ",source)
            # print("target = ",target)
            # if source not in target_nodes_to_remove or target not in target_nodes_to_remove: wrong 
            if source in target_nodes_to_remove or target in target_nodes_to_remove:
                #只要有一个在就说明是悬空的，那就返回False
                return False

    # 所有检查都通过
    return True


def get_applicable_matches(rule, graph):
    """Generates all applicable matches for rule in graph."""
    for match in find_matches(rule, graph):
        # print("match in find_matches = ",match)
        # print("check_rule_applicability(rule, graph, match)",check_rule_applicability(rule, graph, match))
        if check_rule_applicability(rule, graph, match):
            # print("get applicable matches!",match)
            yield match



def has_nonterminals(graph):
    """Returns True if the graph contains nonterminal nodes/edges, and False
    otherwise."""
    initial_node = 'robot'  # 初始节点的名称，根据你的数据进行相应修改

    for node, data in graph.nodes(data=True):
        # 跳过初始节点
        if node == initial_node:
            continue
        
        # print("node,data",node,data)
        if 'shape' not in data.keys():
            # print("has_nonterminals")
            return True
        
    for edge, data in graph.edges(data=True):
        # print("edge,data",edge,data)
        if 'type' not in data.keys():
            # print("has_nonterminals")
            return True
        
    return False

def make_graph(rules, rule_sequence):
    graph = make_initial_graph()
    for r in rule_sequence:
        matches = list(get_applicable_matches(rules[r], graph))
        if matches:
            graph = apply_rule(rules[r], graph, matches[0])
        else:
            raise ValueError("Rule in sequence has no applicable matches")
    return graph