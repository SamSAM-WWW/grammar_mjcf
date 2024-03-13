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
excluded_rules = [0, 1, 2, 3, 4, 10] #需要同步修改apply_rule.py 410行
def predict(state,new_folder_path):
    '''
    输入state, 转换成xml文件后预测值函数并删除中间文件
    '''
    generate_xml_from_R(state,new_folder_path,'xmlrobot_temp')
    xml_out_path = os.path.join(new_folder_path, 'xmlrobot_temp' + "_symm.xml")
    os.remove(xml_out_path)
    predict_val = 0
    #predict
    #predict
    #retun predict Value
    return predict_val


def transite(state,action,rules,target_node_name):
    '''
    从当前图向下一个图转变
    '''
    next_state = apply_rule(rule=rules[action], input_graph=state, target_node_name=target_node_name)
    return next_state

def select_action( state, rules, target_node, eps, new_folder_path):
    '''
    根据选定的目标节点选取可执行的规则
    '''
    available_actions = get_available_actions_for_target_node(rules, target_node)
    if len(available_actions) == 0:
        return None, None
    
    sample = random.random()
    step_type = ""
    if sample > eps:
        # Exploit
        values = []
        next_states = []
        for action in available_actions:
            # 评估每个动作的值
            next_state = transite(state, action, rules, target_node) 
            values.append(predict(next_state,new_folder_path))
            next_states.append(next_state)
        
        # 选择值最大的动作
        best_action_index = np.argmax(values)
        best_action = available_actions[best_action_index]
        step_type = 'optimal'
    else:
        # Explore
        # 随机选择一个动作
        best_action = random.choice(available_actions)
        step_type = 'random'
    
    return best_action

def TF():
    pass
def TF_train():
    pass
def get_last_child_of_subtree(state, node):
    """
    找到某个节点的子树的最后一个子节点（包括该节点本身）。
    """
    if not state.successors(node):
        # 如果节点没有子节点，则返回节点本身
        return node
    last_child = node  # 初始情况下最后一个子节点是节点本身
    stack = [node]  # 使用栈来实现深度优先搜索

    while stack:
        current_node = stack.pop()
        successors = list(state.successors(current_node))
        if successors:
            # 将当前节点的子节点压入栈中
            stack.extend(successors)
            # 更新最后一个子节点
            last_child = current_node

    return last_child

def get_available_actions_for_target_node(rules, target_node):
    available_actions = []

    # 遍历规则列表
    for i, rule in enumerate(rules):
        # 检查当前规则是否适用于目标节点
        if is_rule_applicable_to_target_node(rule, target_node) and rule not in excluded_rules:
            available_actions.append(i)

    return available_actions

def is_rule_applicable_to_target_node(rule, target_node):
    # 检查规则的目标节点是否与给定的目标节点匹配
    matching_keys = [key for key in rule.lhs_nodes if target_node.startswith(key)]
    return len(matching_keys) > 0

def get_reward(selected_design):
    pass

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
            writer.writerow(['xml_out_path', 'hash', 'reward'])
        # 写入数据
        for row in data:
            writer.writerow(row)
def generate_xml_from_R(R,new_folder_path,filename):
    M = RobotModelGen.ModelGenerator(R)
    M.set_compiler(angle='degree',inertiafromgeom='true')
    M.set_size()
    M.set_option(gravity=-9.8)
    M.get_robot_dfs()
    M.generate()
    xml_file_path = os.path.join(new_folder_path, filename + ".xml")
    xml_out_path = os.path.join(new_folder_path, filename + "_symm.xml")
    trans_op(xml_file_path=xml_file_path, xml_out_path=xml_out_path)
    os.remove(xml_file_path)
def search_algo():
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    new_folder_path = os.path.join("mjcf_model", current_time)
    os.makedirs(new_folder_path)
    filename = 'xmlrobot'
    hash_pool = []
    V = TF()
    rules = create_4leg_rules()
    eps_end = 0.1
    eps_start = 1.0
    num_iterations = 1000
    eps_decay= 0.3

    eps_sample_end = 0.1
    eps_sample_start = 1.0
    eps_sample_decay = 0.3

    depth = 40
    for epoch in range(num_iterations):
        t_start = time.time()
        eps = eps_end + (eps_start - eps_end) * np.exp(-1.0 * epoch / num_iterations / eps_decay)
        eps_sample = eps_sample_end + (eps_sample_start - eps_sample_end) * np.exp(-1.0 * epoch / num_iterations / eps_sample_decay)

        t_sample, t_update, t_mpc, t_opt = 0, 0, 0, 0
        selected_design, selected_reward = None, -np.inf
        p = random.random()
        if p < eps_sample:
            num_samples = 1
        else:
            num_samples = 16
        
        # use e-greedy to sample a design within maximum #steps.
        for num in range(num_samples):
            valid = False

            for num_try in range(100):
                t0 = time.time()

                filename = 'xmlrobot' + str(epoch) + '_' + str(num) + '_' + str(num_try)
                state = make_graph_by_step(filename)
                for i in range(depth):
                    
                    if i % 2 == 0:
                        # 偶数，选择 limbmount3 的子树的最后一个子节点
                        target_node = get_last_child_of_subtree(state,'limbmount3')
                        #针对一个特定的target_node 选一个可操作规则
                        action = select_action(state,rules,target_node,eps,new_folder_path)
                    else:
                        # 偶数，选择 limbmount3 的子树的最后一个子节点
                        target_node = get_last_child_of_subtree(state,'limbmount1')
                        #针对一个特定的target_node 选一个可操作规则
                        action = select_action(state,rules,target_node,eps,new_folder_path)
                    next_state = transite(state=state,action=action,rules=rules,target_node_name=target_node)
                    state = next_state




            predicted_value = predict(state)
            if predicted_value > selected_reward:
                selected_design, selected_reward = state, predicted_value
            
        reward,best_reward = -np.inf,None
        filename_4_epoch = 'xmlrobot_' + str(epoch)
        generate_xml_from_R(selected_design,new_folder_path,filename_4_epoch)
        xml_out_path = os.path.join(new_folder_path, filename + "_symm.xml")

        hash_val = calculate_hash_without_first_line(xml_file=xml_out_path)
        if hash_val not in hash_pool:
            hash_pool.append(hash_val)

            reward = get_reward(selected_design=xml_out_path)
            if reward > best_reward:
                best_reward = reward
                best_design = xml_out_path
            data_to_save = []

            data_to_save.append([xml_out_path, hash_val, reward])
            csv_file_path = os.path.join(new_folder_path, 'design_rewards.csv')
            save_to_csv(data_to_save, csv_file_path)


        # optimize
        # train V
        TF_train()