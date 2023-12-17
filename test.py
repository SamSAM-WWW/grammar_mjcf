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
def has_nonterminals(graph):
    for node, data in graph.nodes(data=True):
        if isinstance(data, dict) and 'attrs' in data:
            if 'shape' in data['attrs'] and data['attrs']['shape'] == 'NONE':
                return True
    return False
def make_initial_graph():
    G = nx.DiGraph(name = 'arobot')
    G.add_node('robot',label ='robot',sub = 'L')
    G.add_node('robot',require_label ='robot',sub = 'R')
    print(G.nodes.data())
    return G
    
# Example usage
state = make_initial_graph()
