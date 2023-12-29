'''
RobotGrammarEnv.py

Implement the environment for robot grammar search problem.
'''
# import python packages
import os
import random
from copy import deepcopy
import numpy as np
from new_.apply_rule import *
'''
class RobotGrammarEnv

Parameters:
    task: a task to be evaluated for the design
    rules: collection of grammar rules (actions)
    seed: random seed for the env
    mpc_num_processes: number of threads for mpc
    enable_reward_oracle: whether use the GNN oracle to compute the reward
    preprocessor: the preprocessor concerting a robot_graph into the GNN input, required if enable_reward_oracle is True
'''

class RobotGrammarEnv:
    def __init__(self, rules, seed = 0, enable_reward_oracle = False, preprocessor = None):
        self.rules = rules
        self.seed = seed
        self.rng = random.Random(seed)
        self.enable_reward_oracle = enable_reward_oracle
        if self.enable_reward_oracle:
            assert preprocessor is not None
            self.preprocessor = preprocessor
            self.load_reward_oracle()
        self.initial_state = make_initial_graph()
        self.result_cache = dict()
        self.state = None
        self.rule_seq = []
    
    def reset(self):
        self.state = self.initial_state
        self.rule_seq = []
        return self.state


    def transite(self, action, input_graph, target_node_name  ):

        next_state = apply_rule(self.rules[action], input_graph, target_node_name)
        return next_state

    