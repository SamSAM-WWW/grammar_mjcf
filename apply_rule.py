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


def make_initial_graph():
    G = nx.DiGraph(name = 'arobot')
    G.add_node('robot',label ='robot')
    print(G.nodes.data())
    return G


def apply_rule(rule,target_graph,lhs_to_target):
    result_graph = target_graph.copy()
    #    Copy target nodes not in LHS to result
    lhs_nodes = set(rule.lhs_node.keys())
        # 遍历目标图的节点
    for node in target_graph.nodes(data=True):
        node_name, node_data = node
        # 如果节点不在LHS中，将其复制到结果图中
        if node_name not in lhs_nodes:
            result_graph.add_node(node_name, **node_data)

    result_graph = target_graph.copy()
    return result_graph


def find_matches(rule,graph):
  matches = []
  # 遍历图中的节点
  for node in graph.nodes(data=True):
      node_name, node_data = node

      # 检查节点是否匹配规则的左侧
      if node_name in rule.lhs_node:
          lhs_mapping = rule.lhs_node[node_name]
          match = {'node_mapping': {tuple(lhs_mapping.items()): node_name}}

          matches.append(match)
          print("Debug: Initial matches:", matches)
  return matches


def check_rule_applicability(rule, target_graph, match):
  target_nodes_to_remove = set(match['node_mapping'].values())
  target_edges_in_lhs = set()

  for lhs_edge in rule.lhs_edge:
      lhs_tail, lhs_head = lhs_edge
      lhs_tail_mapped = match['node_mapping'][lhs_tail]
      lhs_head_mapped = match['node_mapping'][lhs_head]
      target_edges_in_lhs.add((lhs_tail_mapped, lhs_head_mapped))

  for target_edge_index, target_edge in enumerate(target_graph.edges()):
      target_edge_head, target_edge_tail = target_edge
      target_edge_in_lhs = (target_edge_tail, target_edge_head) in target_edges_in_lhs

      if not target_edge_in_lhs:
          if target_edge_head in target_nodes_to_remove or target_edge_tail in target_nodes_to_remove:
              return False  # Head or tail node would be removed, making this edge a dangling edge

  return True


def get_applicable_matches(rule, graph):
  """Generates all applicable matches for rule in graph."""
  for match in find_matches(rule, graph):
    if check_rule_applicability(rule, graph, match):
      yield match



def has_nonterminals(graph):
    for node, data in graph.nodes(data=True):
        if isinstance(data, dict) and 'attrs' in data:
            if 'shape' in data['attrs'] and data['attrs']['shape'] == 'NONE':
                return True
            if 'joint_type' in data['attrs'] and data['attrs']['joint_type'] == 'NONE':
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