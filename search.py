from RobotGraph import RobotGraph,RobotJoint,RobotLink
from new_.apply_rule import *
import networkx as nx
import matplotlib.pyplot as plt
import queue
from new_.trans import *
import random
import copy

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

    excluded_rules = [0, 1, 2, 3, 4, 5, 6] #需要同步修改apply_rule.py 410行
    available_nodes = [node for node in R.nodes if 'joint' not in node]
    # print("available_nodes",available_nodes)
    # 如果存在可选节点，则随机选择一个
    if available_nodes:
        selected_node = random.choice(available_nodes)
        # print("selected_node",selected_node)
        # 找到适用于选定节点的规则
        applicable_rules = [action for action in available_actions if is_rule_applicable_target(rules[action], selected_node)]
        applicable_rules = [action for action in applicable_rules if action not in excluded_rules]

        # print("applicable_rules",applicable_rules)
        # 如果存在可应用的规则，则随机选择一个
        if applicable_rules:
            selected_action = random.choice(applicable_rules)
            # print("selected_action",selected_action)
            # 应用规则
            R = apply_rule(rule=rules[selected_action], input_graph=R, target_node_name=selected_node)

    return R


# def copy_subtree(R, source_node, target_node):
#     # 获取 source_node 的所有子节点
#     children = list(R.successors(source_node))

#     # 复制 source_node 及其子节点到 target_node
#     for child in children:
#         print("Edges in R:", R.edges)
#         if ('limbmount1', source_node) in R.edges:
#             print(f"Edge ('limbmount1', {source_node}) found in R.edges.")
#         else:
#             print(f"Error: Edge ('limbmount1', {source_node}) not found in R.edges.")
#         new_child = copy.deepcopy(R.nodes[child]['info'])
#         R.add_node(node_type=R.nodes[child]['type'], node_info=new_child)
#         R.add_edge(target_node, new_child.name)
#         # 递归调用 copy_subtree 函数以复制所有子节点
#         copy_subtree(R, child, new_child.name)

def copy_subtree(R, source_node, target_node_prefix):
    # 获取 source_node 的所有子节点
    children = list(R.successors(source_node))
    if not children:
        return
    # 复制 source_node 及其子节点到 target_node
    for child in children:
        # 生成新节点的名称，确保不与已有节点重复
        new_child_name = f"{target_node_prefix}_new"
        new_child = copy.deepcopy(R.nodes[child]['info'])
        
        # 修改节点名称
        new_child.name = new_child_name
        
        # 添加新节点
        R.add_node(node_type=R.nodes[child]['type'], node_info=new_child)

        # 添加边
        R.add_edge(target_node_prefix, new_child_name)

        # 递归调用 copy_subtree 函数以复制所有子节点
        copy_subtree(R, child, new_child_name)
    
    

def replace_limbmounts_recursive(R, limbmount_node):
    # 获取 limbmount_node 的所有子节点
    # print("Nodes in R:", R.nodes)
    children = list(R.successors(limbmount_node))
    
    
    # 删除当前节点
    R.remove_node(limbmount_node)

    

    # 递归调用 replace_limbmounts_recursive 函数以删除所有子节点
    for child in children:
        replace_limbmounts_recursive(R, child)

def replace_limbmounts(R):
    # 删除 limbmount_2 的子树
    limbmount_2_children = list(R.successors("limbmount2"))
    if limbmount_2_children:
        limbmount_2_first_child = limbmount_2_children[0]
        replace_limbmounts_recursive(R, limbmount_2_first_child)

    # 复制 limbmount_1 的子树到 limbmount_2
    copy_subtree(R, "limbmount1", "limbmount2")

    # 删除 limbmount_4 的子树
    limbmount_4_children = list(R.successors("limbmount4"))
    if limbmount_4_children:
        limbmount_4_first_child = limbmount_4_children[0]
        replace_limbmounts_recursive(R, limbmount_4_first_child)

    # 复制 limbmount_3 的子树到 limbmount_4
    copy_subtree(R, "limbmount3", "limbmount4")

    return R
# 示例用法
def has_child_nodes(graph, node):
    """
    检查给定节点的子节点是否有子节点。
    """
    return any(graph.successors(child) for child in graph.successors(node))
    
def result_R(filename='xmlrobot'):

    R = make_graph_by_step(filename)
    rules = create_4leg_rules_v4()
    available_actions = get_available_actions(R, rules)
    # print("可执行的规则序号：", available_actions)

    random_search(R,rules,available_actions)


    for i in range(100):
        available_actions = get_available_actions(R, rules)
        R = random_search(R,rules,available_actions)

    R = replace_limbmounts(R)
    return R



