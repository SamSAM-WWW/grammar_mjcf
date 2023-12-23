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
import re

from RobotGraph import RobotGraph
from RobotGraph import RobotLink
from RobotGraph import RobotJoint
from rule import create_rules

def make_initial_graph():
    '''
    功能:生成初始机器人图
    ---------------
    输入:无

    输出:初始机器人图 `R` （类型为`RobotGraph`）
    '''
    R = RobotGraph(name='xmlrobot')
    root = RobotLink('root',length=5,size=10)
    R.add_node( node_type='link',node_info = root)
    print(R.nodes)
    return R

def apply_rule(rule,input_graph:RobotGraph ,target_node_name:str):
    '''
    功能:对机器人图进行操作，使用规则后得到新的机器人图
    ---------------
    输入:选定的一个规则`rule`,
    例如
        rule = create_rule(name='make_robot',
                        lhs_nodes={'root':{'require_label':'root'}},

                        lhs_edges=None,

                        rhs_nodes={'body':{'label':'body'}},

                        rhs_edges=None)
        rule的左子图确定操作对象
        rule的右子图确定操作方式
    
    字典 键为；待修改的机器人图`input_graph`（类型为`RobotGraph`）；待修改的节点`target_node_name`

    输出:修改后的机器人图 `result`（类型为`RobotGraph`）
    '''
    result=input_graph
    # 判断输入的 input_graph:RobotGraph 中是否有可操作的 target_node_name
    if target_node_name not in input_graph.nodes:
        print('!target_node_name not in input_graph.nodes!')
    
    else:
        print('target_node_name in input_graph.nodes')
        # 判断输入的 rule 是否匹配 target_node_name
        matching_keys = [key for key in rule.lhs_nodes if target_node_name.startswith(key)]
        if not matching_keys:
            # 无法操作
            print('target_node_name not in rule.lhs_nodes')
        if matching_keys:
            print('target_node_name in rule.lhs_nodes')
            # 对input_graph进行操作
            # 先判断target_node表示link 还是 joint
            # 判断节点类型
            node_info = input_graph.nodes[target_node_name]['info']
            print("node_info.start_point",node_info.start_point)
            if hasattr(node_info, 'link_type'):
                # 处理 link 的操作
                # Copy target nodes in common rule
                prefix = re.match(r'([a-zA-Z]+)', target_node_name).group(1)
                if prefix in rule.common_nodes:
                    # print("------",rule.common_nodes[prefix]['length'])
                    print("Updated info in rule.common_nodes",target_node_name)
                    new_target_node_name = target_node_name
                    new_node = RobotLink(name = target_node_name, length=rule.common_nodes[prefix]['length'] if 'length' in rule.common_nodes[prefix] else 0,
                                        size=rule.common_nodes[prefix]['radius'] if 'radius' in rule.common_nodes[prefix] else 0)
                    result.add_node(node_type='link', node_info=new_node)

                # Add RHS nodes which are not in common with the LHS
                additional_rhs_nodes = {node_name: node_info for node_name, node_info in rule.rhs_nodes.items() if node_name not in rule.common_nodes}    
                print("additional_rhs_nodes",additional_rhs_nodes)
                new_add_node_names = []
                for node_name, node_info in additional_rhs_nodes.items():
                    new_add_node_name = node_name + str(random.randint(1000,9999))
                    new_node = RobotLink(name=new_add_node_name, length=node_info.get('length', 0))
                    result.add_node(node_type='link', rule_label= rule.rhs_nodes[node_name]['label'] if 'label' in rule.rhs_nodes[node_name] else None, node_info=new_node)

                # Copy target edges in LHS to result if they are in common with the RHS
                for edge_info in rule.rhs_edges:
                    from_node = target_node_name
                    to_node = new_add_node_name

                    # 如果有 label，将其添加到新节点的属性中
                    new_node_name = 'joint' + str(random.randint(1000,9999))
                    new_joint = RobotJoint(name=new_node_name, joint_type=edge_info['type'] if 'type' in edge_info else 'hinge',
                                            axis=edge_info['axis'] if 'axis' in edge_info else [1, 0, 0])

                    # 将新的 RobotJoint 实例添加到 result_graph 中
                    result.add_node(node_type='joint',rule_label=edge_info['label'] if 'label' in edge_info else None, node_info=new_joint)

                    # 添加边到 result_graph 中
                    result.add_edge(from_node, new_node_name, **edge_info)
                    result.add_edge(new_node_name, to_node, **edge_info)
                    print(result.nodes)
                    print(result.nodes[new_node_name]['info'].joint_type)

            
            elif hasattr(node_info, 'joint_type'):
                # 处理 joint 的操作
                # TODO: 添加处理 joint 的操作的代码
                print("todo")


    return result








def example_of_apply_rule():

    R = make_initial_graph()
    rules = create_rules()
    #---------------------------------------------------------------------------
    # add the first body 
    R = apply_rule(rule=rules[0],input_graph=R,target_node_name='root')




    #---------------------------------------------------------------------------
    # add a limb_mount on body
    filtered_nodes = [node for node in R.nodes if 'body' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[1],input_graph=R,target_node_name=target_node_name)
    
    filtered_nodes = [node for node in R.nodes if 'body' in node]
    print(filtered_nodes)
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    print(R.nodes[target_node_name]['info'].size)
    print(R.nodes[target_node_name]['info'].length)



    # add a limb on limb_mount
    filtered_nodes = [node for node in R.nodes if 'limb_mount' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[2],input_graph=R,target_node_name=target_node_name)
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # add a limb_mount on body
    filtered_nodes = [node for node in R.nodes if 'body' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[1],input_graph=R,target_node_name=target_node_name)



    # add a limb on limb_mount
    filtered_nodes = [node for node in R.nodes if 'limb_mount' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[2],input_graph=R,target_node_name=target_node_name)
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # add a limb_mount on body
    filtered_nodes = [node for node in R.nodes if 'body' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[1],input_graph=R,target_node_name=target_node_name)




    # add a limb on limb_mount
    filtered_nodes = [node for node in R.nodes if 'limb_mount' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[2],input_graph=R,target_node_name=target_node_name)
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # add a limb_mount on body
    filtered_nodes = [node for node in R.nodes if 'body' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[1],input_graph=R,target_node_name=target_node_name)



    # add a limb on limb_mount
    filtered_nodes = [node for node in R.nodes if 'limb_mount' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[2],input_graph=R,target_node_name=target_node_name)
    #---------------------------------------------------------------------------

    print(R.edges)


example_of_apply_rule()