from RobotGraph import RobotGraph,RobotJoint,RobotLink
from new_.apply_rule import *
import networkx as nx
import matplotlib.pyplot as plt
import queue
from new_.trans import *
import random

def get_available_actions(R, rules):
    available_actions = []

    # 遍历规则列表
    for i, rule in enumerate(rules):
        # 遍历图中的节点
        if is_rule_applicable(rule, R):
            available_actions.append(i)
            # break  # 一旦找到一个可执行的规则，就不再检查当前规则的其他节点

    return available_actions

def is_rule_applicable(rule, input_graph):
    # 遍历图中的所有节点
    for target_node_name in input_graph.nodes:
        # 判断输入的 rule 是否匹配 target_node_name
        matching_keys = [key for key in rule.lhs_nodes if target_node_name.startswith(key)]
        if matching_keys:
            # 存在匹配的节点即可
            return True

    return False

def is_rule_applicable_target(rule, target_node_name):
    # 遍历图中的所有节点
    # 判断输入的 rule 是否匹配 target_node_name
    matching_keys = [key for key in rule.lhs_nodes if target_node_name.startswith(key)]
    if matching_keys:
        # 存在匹配的节点即可
        return True

    return False
def random_search(R, rules, available_actions):
    # 随机选择一个节点
    available_nodes = [node for node in R.nodes if 'joint' not in node]
    print("available_nodes",available_nodes)
    # 如果存在可选节点，则随机选择一个
    if available_nodes:
        selected_node = random.choice(available_nodes)
        print("selected_node",selected_node)
        # 找到适用于选定节点的规则
        applicable_rules = [action for action in available_actions if is_rule_applicable_target(rules[action], selected_node)]
        print("applicable_rules",applicable_rules)
        # 如果存在可应用的规则，则随机选择一个
        if applicable_rules:
            selected_action = random.choice(applicable_rules)
            print("selected_action",selected_action)
            # 应用规则
            R = apply_rule(rule=rules[selected_action], input_graph=R, target_node_name=selected_node)

    return R

# 示例用法
def result_R():

    R = make_graph_by_step()
    rules = create_4leg_rules()
    available_actions = get_available_actions(R, rules)
    print("可执行的规则序号：", available_actions)

    random_search(R,rules,available_actions)
    available_actions = get_available_actions(R, rules)
    print("可执行的规则序号：", available_actions)

    for i in range(100):
        random_search(R,rules,available_actions)
        available_actions = get_available_actions(R, rules)
        print("可执行的规则序号：", available_actions)

    return R



