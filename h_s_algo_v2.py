from uni import UniSimulator

from create_graphs_with_dag import create_graphs
from DAG import *
from collections import OrderedDict
from from_dag_graph_to_rules import *
from RobotGrammarEnv import RobotGrammarEnv
import time
import random
import numpy as np
from apply_rule import *
import sys
import os
from RobotGraph import RobotGraph,RobotJoint,RobotLink
from new_.apply_rule import *
import networkx as nx
import matplotlib.pyplot as plt
import queue
from new_.trans import *
import random
import copy
from mjcf import elements as e
from new_.apply_rule import *
import networkx as nx
import matplotlib.pyplot as plt
import queue
from new_.trans import *
from search import *
from scipy.spatial.transform import Rotation 
import os
import sys
import time
import hashlib
import csv
import RobotModelGen
import xml.etree.ElementTree as ET
from PreProcessor import Preprocessor
from Net import Net
from common import *
from states_pool import StatesPool

import argparse
import time
import random
import pickle
import csv
import numpy as np


import torch
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter
from sklearn.metrics import mean_squared_error


device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
excluded_rules = [0, 1, 2, 3, 4] #需要同步修改apply_rule.py 410行 search.py 45
load_V_path = '/home/ps/pan1/files/Sam/grammar_mjcf-master/mjcf_model/2024-04-12_23-30-25/V_gnn_inpro.pt'
opt_iter = 25 
batch_size = 32
states_pool_capacity = 10000000
reward,best_reward = 0,0


# def predict(state,new_folder_path):
#     '''
#     输入state, 转换成xml文件后预测值函数并删除中间文件
#     '''
#     generate_xml_from_R(state,new_folder_path,'xmlrobot_temp')
#     xml_out_path = os.path.join(new_folder_path, 'xmlrobot_temp' + "_symm.xml")
    
#     predict_val = 0
#     predict_val = random.random()
#     #predict
#     #predict
#     #retun predict Value
#     os.remove(xml_out_path)
#     return predict_val

def pre_train(uni):
    uni.simulate(40000000)

def use_controller(uni):
    return uni.simulate(0)

def update_controller(uni):
    return uni.simulate(8000000)


def update_states_pool(states_pool, state_seq, states_set):
    for state in state_seq:
        state_hash_key = hash(state)
        if not (state_hash_key in states_set):
            states_pool.push(state)
            states_set.add(state_hash_key)

def update_Vhat(V_hat, state_seq, reward):
    for state in state_seq:
        state_hash_key = hash(state)
        if not (state_hash_key in V_hat):
            V_hat[state_hash_key] = -np.inf
        V_hat[state_hash_key] = max(V_hat[state_hash_key], reward)
        # print(f"Updated V_hat[{state_hash_key}]with reward {reward}")

def predict_gnn(V,state):
    global preprocessor
    adj_matrix_np, features_np, _ = preprocessor.preprocess(state)
    masks_np = np.full(len(features_np), True)
    with torch.no_grad():
        features = torch.tensor(features_np).unsqueeze(0)
        adj_matrix = torch.tensor(adj_matrix_np).unsqueeze(0)
        masks = torch.tensor(masks_np).unsqueeze(0)
        
        #turn to float32
        features = features.to(torch.float32)
        adj_matrix = adj_matrix.to(torch.float32)
        masks = masks.to(torch.float32)

        features = features.to(device)
        adj_matrix = adj_matrix.to(device)
        masks = masks.to(device)

        output, _, _ = V(features, adj_matrix, masks)
        return output.item()

def transite(state,action,rules,target_node_name):
    '''
    从当前图向下一个图转变
    '''
    next_state = apply_rule(rule=rules[action], input_graph=state, target_node_name=target_node_name)
    return next_state

def select_action( state, rules, target_node, eps, V):
    '''
    根据选定的目标节点选取可执行的规则
    '''
    available_actions = get_available_actions(state,rules)
    if len(available_actions) == 0:
        # print("No available actions for target node")
        return None
    
    sample = random.random()
    step_type = ""
    applicable_rules = [action for action in available_actions if is_rule_applicable_target(rules[action], target_node)]
    applicable_rules = [action for action in applicable_rules if action not in excluded_rules]
    if applicable_rules:
        if sample > eps:
            # Exploit
            values = []
            next_states = []
            for action in applicable_rules:
                # 评估每个动作的值
                next_state = transite(state, action, rules, target_node) 
                values.append(predict_gnn(V,next_state))
                next_states.append(next_state)
            
            # 选择值最大的动作
            best_action_index = np.argmax(values)
            best_action = available_actions[best_action_index]
            step_type = 'optimal'
        else:
            # Explore
            # 随机选择一个动作
            best_action = random.choice(applicable_rules)
            step_type = 'random'
        # print("best action is ",best_action)
        return best_action
    else:
        return None

# def get_last_child_of_subtree(state, node):
#     """
#     找到某个节点的子树的最后一个子节点（包括该节点本身）。
#     """
#     if not state.successors(node):
#         # 如果节点没有子节点，则返回节点本身
#         return node
#     last_child = node  # 初始情况下最后一个子节点是节点本身
#     stack = [node]  # 使用栈来实现深度优先搜索

#     while stack:
#         current_node = stack.pop()
#         successors = list(state.successors(current_node))
#         if successors:
#             # 将当前节点的子节点压入栈中
#             stack.extend(successors)
#             # 更新最后一个子节点
#             last_child = current_node

#     return last_child

def get_non_joint_child(state, node):
    """
    找到某个节点的一个非 joint 类型的子节点。
    """
    # 获取节点的所有子节点
    successors = list(state.successors(node))
    
    # 遍历子节点，找到第一个非 joint 类型的节点
    for successor in successors:
        if 'joint' not in successor:
            return successor
    
    # 如果没有找到非 joint 类型的子节点，则返回 None
    # print("No non-joint child found for node:", node)
    return node

def get_random_target_node(state):
    available_nodes = [node for node in state.nodes if 'joint' not in node]
    if available_nodes:
        selected_node = random.choice(available_nodes)
    return selected_node
def get_available_actions(R, rules):
    available_actions = []

    # 遍历规则列表
    for i, rule in enumerate(rules):
        # 遍历图中的节点
        if is_rule_applicable(rule, R):
            available_actions.append(i)
            # break  # 一旦找到一个可执行的规则，就不再检查当前规则的其他节点
    applicable_rules = [action for action in available_actions if action not in excluded_rules]
    return applicable_rules

def is_rule_applicable_to_target_node(rule, target_node):
    # 检查规则的目标节点是否与给定的目标节点匹配
    matching_keys = [key for key in rule.lhs_nodes if target_node.startswith(key)]
    return len(matching_keys) > 0

def get_reward(uni,eps,xml_name):
    '''
    输入 uni eps xml_name 输出 1个 reward值
    xml_name:"xmlrobot_0.xml"
    输入文件夹绝对路径，读取文件夹下的所有xml文件，返回reward值 返回一个字典
    字典格式：
        xxxx
        "median_reward":{"xmlrobot_0.xml": 76, "xmlrobot_1.xml": 73}
        xxxx
    从字典里提取出对应xml_name的reward值
    
    '''

    use_or_train = random.random()
    if use_or_train < eps:
        print("use controller")
        reward_dict = use_controller(uni)

    else:
        print("train controller")
        reward_dict = update_controller(uni)

    #median_reward
    reward = reward_dict['median_reward']
    #reward = {"xmlrobot_0.xml": 76, "xmlrobot_1.xml": 73}
    val = reward[xml_name]
    return val

def calculate_hash(xml_content):
    # 计算内容的哈希值
    hash_value = hashlib.sha256(xml_content.encode()).hexdigest()
    return hash_value


def calculate_hash_without_first_line(xml_file):
    # 读取XML文件的内容
    with open(xml_file, 'r') as file:
        xml_content = file.read()

    # 移除第一行
    xml_content_without_first_line = '\n'.join(xml_content.split('\n')[1:])

    # 计算移除第一行后的XML文件的哈希值
    hash_without_first_line = calculate_hash(xml_content_without_first_line)

    return hash_without_first_line
# 调用函数计算XML文件的哈希值

def save_to_csv(data, filename):
    # 检查文件是否存在
    file_exists = os.path.isfile(filename)

    # 打开 CSV 文件，使用不同的模式（追加或新建）
    with open(filename, mode='a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)
        # 如果文件是新建的，则写入列标题
        if not file_exists:
            writer.writerow(['xml_out_path', 'hash', 'reward','predict_reward'])
        # 写入数据
        for row in data:
            writer.writerow(row)
def generate_xml_from_R(R,new_folder_path,filename):
    R = replace_limbmounts(R)

    M = RobotModelGen.ModelGenerator(R)
    M.set_compiler(angle='degree',inertiafromgeom='true')
    M.set_size()
    M.set_option(gravity=-9.8)
    M.get_robot_dfs()
    M.generate_2_folder(new_folder_path,filename)
    xml_file_path = os.path.join(new_folder_path, filename + ".xml")
    # xml_out_path = os.path.join(new_folder_path, filename + "_symm.xml")
    # trans_op(xml_file_path=xml_file_path, xml_out_path=xml_out_path)
    # tree = ET.parse(xml_out_path)
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    target_body = root.find(".//body[@name='root']")
    target_body.set('quat', '0.707 0.0 0.0 -0.707')
    # tree.write(xml_out_path)
    tree.write(xml_file_path)
    # os.remove(xml_file_path)
    # print("Generate xml file successfully!")


def test_R_gen():
    filename = 'xmlrobot_'
    R = result_R(filename)
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    new_folder_path = os.path.join("mjcf_model", current_time)
    generate_xml_from_R(R,new_folder_path,filename)
def search_algo():
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    new_folder_path = os.path.join("mjcf_model", current_time)
    os.makedirs(new_folder_path)

    log_dir = new_folder_path  # 日志文件夹路径
    # 创建 SummaryWriter 对象时指定 log_dir
    writer = SummaryWriter(log_dir=log_dir)


    filename = 'xmlrobot'
    # rules = create_4leg_rules()
    rules = create_4leg_rules_v2()

    best_reward = -np.inf



    all_labels = set()
    for rule in rules:
        for node_name, node_attrs in rule.lhs_nodes.items():
            if 'require_label' in node_attrs:
                all_labels.add(node_attrs['require_label'])
        for node_name, node_attrs in rule.rhs_nodes.items():
            if 'require_label' in node_attrs:
                all_labels.add(node_attrs['require_label'])
    all_labels = sorted(list(all_labels))
    global preprocessor
    preprocessor = Preprocessor(all_labels = all_labels)
    max_nodes = 80
    state = make_graph_by_step(filename)
    sample_adj_matrix, sample_features, sample_masks = preprocessor.preprocess(state)
    num_features = sample_features.shape[1]
    V = Net(max_nodes=max_nodes, num_channels = num_features,num_outputs = 1 ).to(device)
    
    if load_V_path is not None:
        V.load_state_dict(torch.load(load_V_path))
        print_info('Loaded pretrained V function from {}'.format(load_V_path))


    # initialize target V_hat look up table
    V_hat = dict()
    # initialize states_pool
    states_pool = StatesPool(capacity = states_pool_capacity)
    states_set = set()

    hash_pool = []
    
    eps_end = 0.1
    eps_start = 1.0
    num_iterations = 100
    eps_decay= 0.3

    eps_sample_end = 0.1
    eps_sample_start = 1.0
    eps_sample_decay = 0.3
    pre_pool = {}
    depth = 20
    repeated_cnt = 0

    reward_list = []
    selected_reward_list = []


    #生成100个初始模型 并且预训练控制器
    for i in range(100):
        filename = 'xmlrobot_pre_' + str(i)
        R = result_R(filename)
        M = RobotModelGen.ModelGenerator(R)
        M.set_compiler(angle='degree',inertiafromgeom='true')
        M.set_size()
        M.set_option(gravity=-9.8)
        M.get_robot_dfs()
        M.generate_2_folder(new_folder_path, filename)
        print(M.compiler.angle)
        xml_file_path = os.path.join(new_folder_path, filename + ".xml")
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        target_body = root.find(".//body[@name='root']")
        target_body.set('quat', '0.707 0.0 0.0 -0.707')
        tree.write(xml_file_path)
    
    uni = UniSimulator(new_folder_path)
    pre_train(uni)
    print("pre-train finished!")     



    for epoch in range(num_iterations):
        V.eval()
        t_start = time.time()
        eps = eps_end + (eps_start - eps_end) * np.exp(-1.0 * epoch / num_iterations / eps_decay)
        eps_sample = eps_sample_end + (eps_sample_start - eps_sample_end) * np.exp(-1.0 * epoch / num_iterations / eps_sample_decay)

        t_sample, t_update, t_mpc, t_opt = 0, 0, 0, 0
        selected_design, selected_reward = None, -np.inf
        p = random.random()
        if p < eps_sample:
            num_samples = 10
        else:
            num_samples = 40
        best_state = None

        
        global optimizer
        optimizer = torch.optim.Adam(V.parameters(), lr = 1e-4)
        best_pre_val = float('-inf')  # 初始化最佳预测值为负无穷大
        # use e-greedy to sample a design within maximum #steps.
        for num in range(num_samples):
            # for num_try in range(100):
            t0 = time.time()
            
            filename = 'xmlrobot' + str(epoch) + '_' + str(num)
            # filename = 'xmlrobot' + str(epoch) + '_' + str(num) + '_' + str(num_try)
            if best_state is None:
                state = make_graph_by_step(filename)
            else: state = best_state
            state_seq = [state]

            #找到当前状态下，最优的下一步设计
            for i in range(depth):
                available_actions = get_available_actions(state, rules) 
                #todo true hs
                next_state = random_search(state,rules,available_actions)
                state_seq.append(next_state)
                pre_val = predict_gnn(V,next_state)
                # 更新最佳预测值和对应的状态
                if pre_val > best_pre_val:
                    best_pre_val = pre_val
                    best_state = next_state








            # predicted_value = predict(best_state,new_folder_path)
            predicted_value = predict_gnn(V,best_state)
            # print("predicted_value:",predicted_value)
            if predicted_value > selected_reward:
                selected_design, selected_reward = state, predicted_value
                selected_state_seq = state_seq
        

        
        filename_4_epoch = 'xmlrobot_' + str(epoch)

        # create a folder for each design to train
        # epoch_folder_path = os.path.join(new_folder_path, f"epoch_{epoch}")

        generate_xml_from_R(selected_design,new_folder_path,filename_4_epoch)


        xml_name = filename_4_epoch + '.xml'
        reward = get_reward(uni,eps,xml_name)
        print(f"predict-reward:{selected_reward},current-design:{epoch},reward-for-current-design:{reward}")
        if reward > best_reward:
            best_reward = reward

        data_to_save = []
        writer.add_scalar("Predicted Reward", selected_reward, epoch)
        writer.add_scalar("Actual Reward", reward, epoch)
        writer.add_scalar("Reward Difference", reward - selected_reward, epoch)
        reward_list.append(reward)
        selected_reward_list.append(selected_reward)
        reward_array = np.array(reward_list)
        selected_reward_array = np.array(selected_reward_list)
        rmse = np.sqrt(mean_squared_error(selected_reward_array, reward_array))
        writer.add_scalar("RMSE", rmse, epoch)

        update_Vhat(V_hat, selected_state_seq, reward)
        update_states_pool(states_pool, selected_state_seq, states_set)
        hash_val = hash(selected_design)
        data_to_save.append([xml_name, hash_val, reward, selected_reward])
        csv_file_path = os.path.join(new_folder_path, 'design_rewards.csv')
        save_to_csv(data_to_save, csv_file_path)
        # optimize train estimator

        V.train()
        total_loss = 0.0
        for _ in range(opt_iter):
            minibatch = states_pool.sample(min(len(states_pool), batch_size))
            train_adj_matrix, train_features, train_masks, train_reward = [], [], [], []
            max_nodes = 0
            for robot_graph in minibatch:
                hash_key = hash(robot_graph)
                # print("hash_key:",hash_key)
                target_reward = V_hat[hash_key]
                adj_matrix, features, _ = preprocessor.preprocess(robot_graph)
                max_nodes = max(max_nodes, len(features))
                train_adj_matrix.append(adj_matrix)
                train_features.append(features)
                train_reward.append(target_reward)

            for i in range(len(minibatch)):
                train_adj_matrix[i], train_features[i], masks = \
                    preprocessor.pad_graph(train_adj_matrix[i], train_features[i], max_nodes)
                train_masks.append(masks)

            train_adj_matrix_torch = torch.tensor(train_adj_matrix)
            train_features_torch = torch.tensor(train_features)
            train_masks_torch = torch.tensor(train_masks)
            train_reward_torch = torch.tensor(train_reward)
            
            train_adj_matrix_torch = train_adj_matrix_torch.to(torch.float32)
            train_features_torch = train_features_torch.to(torch.float32)
            train_masks_torch = train_masks_torch.to(torch.float32)
            train_reward_torch = train_reward_torch.to(torch.float32)

            train_adj_matrix_torch = train_adj_matrix_torch.to(device)
            train_features_torch = train_features_torch.to(device)
            train_masks_torch = train_masks_torch.to(device)
            train_reward_torch = train_reward_torch.to(device)


            optimizer.zero_grad()
            output, loss_link, loss_entropy = V(train_features_torch, train_adj_matrix_torch, train_masks_torch)
            loss = F.mse_loss(output[:, 0], train_reward_torch)
            loss.backward()
            total_loss += loss.item()
            optimizer.step()

            #save gnn - pt file
            temp_save_path = os.path.join(new_folder_path, 'V_gnn_inpro.pt')
            torch.save(V.state_dict(), temp_save_path)

    #save gnn - pt file
    save_path = os.path.join(new_folder_path, 'V_gnn_final.pt')
    torch.save(V.state_dict(), save_path)
    exit_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    print(f"Start time:{current_time}")
    print(f"Exit time: {exit_time}")
    writer.close()


if __name__ == '__main__':
    search_algo()
    # reward = get_reward(folder_path='/home/ps/pan1/files/Sam/grammar_mjcf-master/mjcf_model/2024-04-12_18-17-37/epoch_0')
    # print('test_reward',reward)