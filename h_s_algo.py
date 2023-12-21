from create_graphs_with_dag import create_graphs
from DAG import *
from collections import OrderedDict
from from_dag_graph_to_rules import *
from RobotGrammarEnv import RobotGrammarEnv
import time
import random
import torch
import numpy as np
from apply_rule import *
import sys
import os


def predict(V, state):
    global preprocessor
    adj_matrix_np, features_np, _ = preprocessor.preprocess(state)
    masks_np = np.full(len(features_np), True)
    with torch.no_grad():
        features = torch.tensor(features_np).unsqueeze(0)
        adj_matrix = torch.tensor(adj_matrix_np).unsqueeze(0)
        masks = torch.tensor(masks_np).unsqueeze(0)
        output, _, _ = V(features, adj_matrix, masks)
        return output.item()

def predict_batch(V, states):
    global preprocessor
    adj_matrix_np, features_np, masks_np = [], [], []
    max_nodes = 0
    for state in states:
        adj_matrix, features, _ = preprocessor.preprocess(state)
        max_nodes = max(max_nodes, len(features))
        adj_matrix_np.append(adj_matrix)
        features_np.append(features)

    for i in range(len(states)):
        adj_matrix_np[i], features_np[i], masks = \
            preprocessor.pad_graph(adj_matrix_np[i], features_np[i], max_nodes)
        masks_np.append(masks)

    with torch.no_grad():
        adj_matrix = torch.tensor(adj_matrix_np)
        features = torch.tensor(features_np)
        masks = torch.tensor(masks_np)
        output, _, _ = V(features, adj_matrix, masks)
    return output[:, 0].detach().numpy()

# def select_action(env, V, state, eps):
#     available_actions = env.get_available_actions(state)
#     if len(available_actions) == 0:
#         return None, None
#     sample = random.random()
#     step_type = ""
#     if sample > eps:
#         next_states = []
#         for action in available_actions:
#             next_states.append(env.transite(state, action))
#         values = predict_batch(V, next_states)
#         best_action = available_actions[np.argmax(values)]
#         step_type = 'optimal'
#     else:
#         best_action = available_actions[random.randrange(len(available_actions))]
#         step_type = 'random'
    
#     return best_action, step_type

def select_action(env, state):
    available_actions = env.get_available_actions(state)
    print("available actions = ",available_actions)
    best_action = available_actions[random.randrange(len(available_actions))]
    step_type = 'random'
    
    return best_action, step_type

def update_Vhat(args, V_hat, state_seq, reward):
    for state in state_seq:
        state_hash_key = hash(state)
        if not (state_hash_key in V_hat):
            V_hat[state_hash_key] = -np.inf
        V_hat[state_hash_key] = max(V_hat[state_hash_key], reward)

def update_states_pool(states_pool, state_seq, states_set):
    for state in state_seq:
        state_hash_key = hash(state)
        if not (state_hash_key in states_set):
            states_pool.push(state)
            states_set.add(state_hash_key)

def search_algo():
    graph_choose = 1
    num_samples = 16
    graphs = create_graphs(graph_choose)
    # for i in range(int(len(graphs))):
    #     graph_i = graphs[i]
    #     print(f"=================graph{i}====================")
    #     rule = create_rule_from_graph(graph_i)
    rules = [create_rule_from_graph(g) for g in graphs]
    env = RobotGrammarEnv(rules)
    state = env.reset()
    # use e-greedy to sample a design within maximum #steps.
    no_action_samples = 0
    step_exceeded_samples = 0
    self_collision_samples = 0
    num_invalid_samples = 0
    num_valid_samples = 0
    num_samples_interval = 0
    t_sample = 0 
    t_update = 0
    last_checkpoint = -1



    save_dir = './trained_models/'
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    design_csv_path = os.path.join(save_dir, 'designs.csv')
    if not os.path.exists(design_csv_path):
        fp_csv = open(design_csv_path, 'w')
        fieldnames = ['rule_seq', 'reward', 'opt_seed']
        writer = csv.DictWriter(fp_csv, fieldnames=fieldnames)
        writer.writeheader()
        fp_csv.close()

    designs = []
    design_rewards = []
    design_opt_seeds = []





    for epoch in range(2):
        t_start = time.time()

        # V.eval()

        # update eps and eps_sample
        # if args.eps_schedule == 'linear-decay':
        #     eps = args.eps_start + epoch / args.num_iterations * (args.eps_end - args.eps_start)
        # elif args.eps_schedule == 'exp-decay':
        #     eps = args.eps_end + (args.eps_start - args.eps_end) * np.exp(-1.0 * epoch / args.num_iterations / args.eps_decay)

        # if args.eps_sample_schedule == 'linear-decay':
        #     eps_sample = args.eps_sample_start + epoch / args.num_iterations * (args.eps_sample_end - args.eps_sample_start)
        # elif args.eps_sample_schedule == 'exp-decay':
        #     eps_sample = args.eps_sample_end + (args.eps_sample_start - args.eps_sample_end) * np.exp(-1.0 * epoch / args.num_iterations / args.eps_sample_decay)

        t_sample, t_update, t_mpc, t_opt = 0, 0, 0, 0

        selected_design, selected_reward = None, -np.inf
        selected_state_seq, selected_rule_seq = None, None

        # p = random.random()
        # if p < eps_sample:
        #     num_samples = 1
        # else:
        #     num_samples = args.num_samples


        for _ in range(num_samples):
            valid = False
            while not valid:
                t0 = time.time()

                state = env.reset()
                rule_seq = []
                state_seq = [state]
                no_action_flag = False
                # print("current num",_)
                for _ in range(3):
                    # print("current num",_)
                    action, step_type = select_action(env, state)
                    print("action is ", action )
                    if action is None:
                        no_action_flag = True
                        break
                    rule_seq.append(action)
                    next_state = env.transite(state, action)
                    print("next_state = ",next_state.nodes)
                    state_seq.append(next_state)
                    state = next_state
                    if not has_nonterminals(state):
                        print("state = next_state not has nonterminals")
                        break
                    print("state = next_state has nonterminals")
                valid = env.is_valid(state)
                
                t_sample += time.time() - t0

                t0 = time.time()

                if not valid:
                    # update the invalid sample's count
                    if no_action_flag:
                        no_action_samples += 1
                    elif has_nonterminals(state):
                        step_exceeded_samples += 1
                    else:
                        self_collision_samples += 1
                    num_invalid_samples += 1
                else:
                    num_valid_samples += 1
                
                num_samples_interval += 1

                t_update += time.time() - t0

            selected_design = state
            selected_rule_seq, selected_state_seq = rule_seq, state_seq
            designs.append(selected_rule_seq)



            # save explored design and its reward
            fp_csv = open(design_csv_path, 'a')
            fieldnames = ['rule_seq', 'reward', 'opt_seed']
            writer = csv.DictWriter(fp_csv, fieldnames=fieldnames)
            print("last_checkpoint+1=",last_checkpoint+1)
            print("len(designs)=",len(designs))
            for i in range(last_checkpoint + 1, len(designs)):
                print("writing data")
                writer.writerow({'rule_seq': str(designs[i]), 'reward': None, 'opt_seed':None})
            last_checkpoint = len(designs) - 1
            fp_csv.close()















search_algo()

