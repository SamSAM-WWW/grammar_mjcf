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

G = nx.DiGraph(name = 'arobot')
G.add_node('robot',label ='robot')
G.add_node('robot',label ='123123')
G.add_node('robot',label ='robot2')
print(G.nodes.data())

