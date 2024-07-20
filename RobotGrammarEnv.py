'''
RobotGrammarEnv.py

Implement the environment for robot grammar search problem.
'''
# import python packages
import os
import random
from copy import deepcopy
import numpy as np
from apply_rule import *
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


    def transite(self, state, action):
        applicable_matches = list(get_applicable_matches(self.rules[action], state))
        # print("transite applicable_matches = ",applicable_matches)
        # print("self.rules[action]",self.rules[action].name)
        # print("applicable_matches[0]",applicable_matches[0])
        next_state = apply_rule(self.rules[action], state, applicable_matches[0])
        return next_state

    def get_available_actions(self, state):
        actions = []
        for idx, rule in enumerate(self.rules):
            # print("idx = ",idx)
            # print("rule = ", rule.name)
            
            applicable_matches = list(get_applicable_matches(rule, state))
            # print("get_available_actions applicable_matches =", applicable_matches)
            if list(get_applicable_matches(rule, state)):         
                actions.append(idx)
        return np.array(actions)
    
    def is_valid(self, state):
        if has_nonterminals(state):
            return False
        else: 
            return True
            #  TODO check self collision