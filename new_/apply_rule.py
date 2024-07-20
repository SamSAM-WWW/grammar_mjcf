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
from new_.rule import *

def make_initial_graph(filename='xmlrobot'):
    '''
    功能:生成初始机器人图
    ---------------
    输入:自定义的xml文件名

    输出:初始机器人图 `R` （类型为`RobotGraph`）
    '''
    R = RobotGraph(name=filename)
    root = RobotLink('root',link_type = 'sphere',size=0.025,body_pos=[0,0,2],geom_pos=[0,0,0],label='root')
    R.add_node( node_type='link',node_info = root)
    # print(R.nodes)
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


    # Check if a body already exists
    existing_bodies = [node for node in result.nodes if 'body' in node]
    if existing_bodies and rule.name in ['make_robot']:
        # Body already exists, don't apply the rule
        # print('Body already exists. Rule not applied.')
        return result




    # 判断输入的 input_graph:RobotGraph 中是否有可操作的 target_node_name
    if target_node_name not in input_graph.nodes:
        print('!target_node_name not in input_graph.nodes!')
    
    else:
        # print('target_node_name in input_graph.nodes')
        # 判断输入的 rule 是否匹配 target_node_name
        matching_keys = [key for key in rule.lhs_nodes if target_node_name.startswith(key)]
        if not matching_keys:
            # 无法操作
            print('target_node_name not in rule.lhs_nodes')
        if matching_keys:
            # print(f'target_node_name = {target_node_name} in rule.lhs_nodes')
            # 对input_graph进行操作
            # 先判断target_node表示link 还是 joint
            # 判断节点类型
            node_info = input_graph.nodes[target_node_name]
            # print(node_info)
            node_info = input_graph.nodes[target_node_name]['info']
            # print("node_info.start_point",node_info.start_point)

            # 新添加的检查
            existing_children = list(result.successors(target_node_name))
            multi_target = 0
            if 'body'  in target_node_name:
                multi_target = 1
            if 'hand_link_2' in target_node_name:
                multi_target = 1
            if existing_children and multi_target==0 :
                # 如果已经有子节点且target_node_name名字不包含 'body'，直接返回
                # print(f'{target_node_name} already has a child. Rule not applied.')
                return result


            if hasattr(node_info, 'link_type'):
                # 处理 link 的操作
                # Copy target nodes in common rule
                prefix = re.match(r'([a-zA-Z]+)', target_node_name).group(1)
                if prefix in rule.common_nodes:
                    if 'body_pos' in rule.common_nodes[prefix] and rule.common_nodes[prefix]['body_pos'] == 'parent':
                        parent_node = input_graph.nodes[target_node_name]['info']
                        parent_length = parent_node.length
                        body_pos = [parent_length + 0.1 , 0, 0]
                    elif 'body_pos' in rule.common_nodes[prefix] and rule.common_nodes[prefix]['body_pos'] == 'wheel-parent':
                        parent_node = input_graph.nodes[target_node_name]['info']
                        parent_length = parent_node.length
                        body_pos = [parent_length + 0.1 , 0, -0.04]
                    elif 'body_pos' in rule.common_nodes[prefix] and rule.common_nodes[prefix]['body_pos'] == 'flat-parent':
                        parent_node = input_graph.nodes[target_node_name]['info']
                        parent_length = parent_node.length
                        body_pos = [parent_length  , 0.08, 0]
                    else:
                        body_pos = rule.common_nodes[prefix]['body_pos'] if 'body_pos' in rule.common_nodes[prefix] else [0, 0, 0]
                    # print("------",rule.common_nodes[prefix]['length'])
                    # print("Updated info in rule.common_nodes",target_node_name)
                    new_target_node_name = target_node_name
                    new_node = RobotLink(name = target_node_name,
                                        link_type= rule.common_nodes[prefix]['shape'] if 'shape' in rule.common_nodes[prefix] else 'capsule',
                                        length=rule.common_nodes[prefix]['length'] if 'length' in rule.common_nodes[prefix] else 0,
                                        size=rule.common_nodes[prefix]['radius'] if 'radius' in rule.common_nodes[prefix] else 0,
                                        geom_pos=rule.common_nodes[prefix]['geom_pos'] if 'geom_pos' in rule.common_nodes[prefix] else [0,0,0],
                                        body_pos=body_pos,
                                        density=rule.common_nodes[prefix]['density'] if 'density' in rule.common_nodes[prefix] else 1000)
                    result.add_node(node_type='link', node_info=new_node)

                # Add RHS nodes which are not in common with the LHS
                additional_rhs_nodes = {node_name: node_info for node_name, node_info in rule.rhs_nodes.items() if node_name not in rule.common_nodes}    
                # print("additional_rhs_nodes",additional_rhs_nodes)
                new_add_node_names = []
                for node_name, node_info in additional_rhs_nodes.items():
                    existing_joint_nodes = [node_name_i for node_name_i in result.nodes if node_name in node_name_i]
                    n = len(existing_joint_nodes)
                    new_add_node_name = node_name + str(n + 1)

                    if 'body_pos' in rule.rhs_nodes[node_name] and rule.rhs_nodes[node_name]['body_pos'] == 'parent':
                        parent_node = input_graph.nodes[target_node_name]['info']
                        parent_length = parent_node.length
                        body_pos = [parent_length + 0.1 , 0, 0]
                    elif 'body_pos' in rule.rhs_nodes[node_name] and rule.rhs_nodes[node_name]['body_pos'] == 'wheel-parent':
                        parent_node = input_graph.nodes[target_node_name]['info']
                        parent_length = parent_node.length
                        body_pos = [parent_length + 0.1 , 0, -0.04]
                    elif 'body_pos' in rule.rhs_nodes[node_name] and rule.rhs_nodes[node_name]['body_pos'] == 'flat-parent':
                        parent_node = input_graph.nodes[target_node_name]['info']
                        parent_length = parent_node.length
                        body_pos = [parent_length , 0.08 , 0]
                    else:
                        body_pos = rule.rhs_nodes[node_name]['body_pos'] if 'body_pos' in rule.rhs_nodes[node_name] else [0, 0, 0]
                    new_node = RobotLink(name = new_add_node_name,
                                        link_type= rule.rhs_nodes[node_name]['shape'] if 'shape' in rule.rhs_nodes[node_name] else 'capsule',
                                        length=rule.rhs_nodes[node_name]['length'] if 'length' in rule.rhs_nodes[node_name] else 0,
                                        size=rule.rhs_nodes[node_name]['radius'] if 'radius' in rule.rhs_nodes[node_name] else 0,
                                        geom_pos=rule.rhs_nodes[node_name]['geom_pos'] if 'geom_pos' in rule.rhs_nodes[node_name] else [0,0,0],
                                        body_pos=body_pos,
                                        euler=rule.rhs_nodes[node_name]['euler'] if 'euler' in rule.rhs_nodes[node_name] else [0,0,0],
                                        geom_euler=rule.rhs_nodes[node_name]['geom_euler'] if 'geom_euler' in rule.rhs_nodes[node_name] else [0,0,0],
                                        label=rule.rhs_nodes[node_name]['label'] if 'label' in rule.rhs_nodes[node_name] else None,
                                        density=rule.rhs_nodes[node_name]['density'] if 'density' in rule.rhs_nodes[node_name] else 500)
                    result.add_node(node_type='link', rule_label= rule.rhs_nodes[node_name]['label'] if 'label' in rule.rhs_nodes[node_name] else None, node_info=new_node)

                # Copy target edges in LHS to result if they are in common with the RHS
                for edge_info in rule.rhs_edges:
                    from_node = target_node_name
                    to_node = new_add_node_name

                    # 如果有 label，将其添加到新节点的属性中
                    existing_joint_nodes = [node_name for node_name in result.nodes if 'joint' in node_name]
                    n = len(existing_joint_nodes)
                    new_node_name = 'joint' + str(n + 1)

                    new_joint = RobotJoint(name=new_node_name, joint_type=edge_info['type'] if 'type' in edge_info else 'hinge',
                                            axis=edge_info['axis'] if 'axis' in edge_info else [1, 0, 0],
                                            stiffness=edge_info['stiffness'] if 'stiffness' in edge_info else None,
                                            damping=edge_info['damping'] if 'damping' in edge_info else None,
                                            joint_range = edge_info['range'] if 'range' in edge_info else None,
                                            ctrlrange = edge_info['ctrlrange'] if 'ctrlrange' in edge_info else [-1,1],
                                            gear = edge_info['gear'] if 'gear' in edge_info else 22.5,)

                    # 将新的 RobotJoint 实例添加到 result_graph 中
                    result.add_node(node_type='joint',rule_label=edge_info['label'] if 'label' in edge_info else None, node_info=new_joint)

                    # 添加边到 result_graph 中
                    result.add_edge(from_node, new_node_name, **edge_info)
                    result.add_edge(new_node_name, to_node, **edge_info)
                    # print(result.nodes)
                    # print(result.nodes[new_node_name]['info'].joint_type)

            
            elif hasattr(node_info, 'joint_type'):
                # 处理 joint 的操作
                # TODO: 添加处理 joint 的操作的代码
                print("todo")


    return result








def example_of_apply_rule():

    R = make_initial_graph()
    rules = create_4leg_rules_v4()
    #---------------------------------------------------------------------------
    # add the first body 
    R = apply_rule(rule=rules[0],input_graph=R,target_node_name='root')




    #---------------------------------------------------------------------------
    # add a limbmount1 on body 右前
    filtered_nodes = [node for node in R.nodes if 'body' in node]
    # print("---",filtered_nodes)
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[1],input_graph=R,target_node_name=target_node_name)
    
    filtered_nodes = [node for node in R.nodes if 'body' in node]
    # print(filtered_nodes)
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    # print('R.nodes[target_node_name][info].size',R.nodes[target_node_name]['info'].size)
    # print('R.nodes[target_node_name][info].length',R.nodes[target_node_name]['info'].length)



    # add a motor on limbmount
    filtered_nodes = [node for node in R.nodes if 'limbmount' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[8],input_graph=R,target_node_name=target_node_name)
    #add a limb on motor
    filtered_nodes = [node for node in R.nodes if  'motor' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[11],input_graph=R,target_node_name=target_node_name)

    #add a motor on limb
    filtered_nodes = [node for node in R.nodes if  'limb' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[9],input_graph=R,target_node_name=target_node_name)

    # #add a thin leg
    # filtered_nodes = [node for node in R.nodes if  'motor' in node]
    # if filtered_nodes:
    #     target_node_name = filtered_nodes[-1]
    # R = apply_rule(rule=rules[6],input_graph=R,target_node_name=target_node_name)
    #     #add a motor on limb
    # filtered_nodes = [node for node in R.nodes if  'limb' in node]
    # if filtered_nodes:
    #     target_node_name = filtered_nodes[-1]
    # R = apply_rule(rule=rules[9],input_graph=R,target_node_name=target_node_name)

    #add a short leg
    filtered_nodes = [node for node in R.nodes if  'motor' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[13],input_graph=R,target_node_name=target_node_name)
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # add a limbmount2 on body 左前
    filtered_nodes = [node for node in R.nodes if 'body' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[2],input_graph=R,target_node_name=target_node_name)



    # add a motor on limbmount
    filtered_nodes = [node for node in R.nodes if 'limbmount' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[8],input_graph=R,target_node_name=target_node_name)
    #add a limb on motor
    filtered_nodes = [node for node in R.nodes if  'motor' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[11],input_graph=R,target_node_name=target_node_name)

    #add a motor on limb
    filtered_nodes = [node for node in R.nodes if  'limb' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[9],input_graph=R,target_node_name=target_node_name)

    # #add a thin leg
    # filtered_nodes = [node for node in R.nodes if  'motor' in node]
    # if filtered_nodes:
    #     target_node_name = filtered_nodes[-1]
    # R = apply_rule(rule=rules[6],input_graph=R,target_node_name=target_node_name)

    # #add a motor on limb
    # filtered_nodes = [node for node in R.nodes if  'limb' in node]
    # if filtered_nodes:
    #     target_node_name = filtered_nodes[-1]
    # R = apply_rule(rule=rules[9],input_graph=R,target_node_name=target_node_name)

    #add a short leg
    filtered_nodes = [node for node in R.nodes if  'motor' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[13],input_graph=R,target_node_name=target_node_name)
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # add a limbmount3 on body 右后
    filtered_nodes = [node for node in R.nodes if 'body' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[3],input_graph=R,target_node_name=target_node_name)




    # add a motor on limbmount
    filtered_nodes = [node for node in R.nodes if 'limbmount' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[8],input_graph=R,target_node_name=target_node_name)
    #add a limb on motor
    filtered_nodes = [node for node in R.nodes if  'motor' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[11],input_graph=R,target_node_name=target_node_name)

    #add a motor on limb
    filtered_nodes = [node for node in R.nodes if  'limb' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[9],input_graph=R,target_node_name=target_node_name)

    #add a thin leg
    filtered_nodes = [node for node in R.nodes if  'motor' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[6],input_graph=R,target_node_name=target_node_name)
        #add a motor on limb
    filtered_nodes = [node for node in R.nodes if  'limb' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[9],input_graph=R,target_node_name=target_node_name)

    #add a short leg
    filtered_nodes = [node for node in R.nodes if  'motor' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[13],input_graph=R,target_node_name=target_node_name)
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # add a limbmount4 on body 左后
    filtered_nodes = [node for node in R.nodes if 'body' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[4],input_graph=R,target_node_name=target_node_name)



    # add a motor on limbmount
    filtered_nodes = [node for node in R.nodes if 'limbmount' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]

    R = apply_rule(rule=rules[8],input_graph=R,target_node_name=target_node_name)
    #add a limb on motor
    filtered_nodes = [node for node in R.nodes if  'motor' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[11],input_graph=R,target_node_name=target_node_name)

    #add a motor on limb
    filtered_nodes = [node for node in R.nodes if  'limb' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[9],input_graph=R,target_node_name=target_node_name)

    #add a thin leg
    filtered_nodes = [node for node in R.nodes if  'motor' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[6],input_graph=R,target_node_name=target_node_name)
        #add a motor on limb
    filtered_nodes = [node for node in R.nodes if  'limb' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[9],input_graph=R,target_node_name=target_node_name)

    #add a short leg
    filtered_nodes = [node for node in R.nodes if  'motor' in node]
    if filtered_nodes:
        target_node_name = filtered_nodes[-1]
    R = apply_rule(rule=rules[13],input_graph=R,target_node_name=target_node_name)
    #---------------------------------------------------------------------------



    # for node in R.nodes:
    #     # print('---------------------------')
    #     # print(node)
    #     node_info = R.nodes[str(node)]['info']
        
    #     if hasattr(node_info, 'link_type'):
    #         print("link_type",R.nodes[str(node)]['info'].link_type)
    #         print("start_point",R.nodes[str(node)]['info'].start_point)
    #         print("end_point",R.nodes[str(node)]['info'].end_point)
    #         print("geom_pos",R.nodes[str(node)]['info'].geom_pos)
    #         print("body_pos",R.nodes[str(node)]['info'].body_pos)
    #         print("euler",R.nodes[str(node)]['info'].euler)
    #         print("size",R.nodes[str(node)]['info'].size)
    #     if hasattr(node_info, 'joint_type'):
    #         print("joint_type",R.nodes[str(node)]['info'].joint_type)
    #         print("axis",R.nodes[str(node)]['info'].axis)
    #         print("pos",R.nodes[str(node)]['info'].pos)
    #         print("joint_range",R.nodes[str(node)]['info'].joint_range)

    # print('+++++++++++++++++++++++++++++++++++++')
    # print(R.edges)
    return R

    



def make_graph_by_step(filename='xmlrobot'):
    '''
    输入：自定义的xml文件名

    输出：最基本的机器人结构
    '''
    R = make_initial_graph(filename)
    rules = create_4leg_rules_v8()
    
    #---------------------------------------------------------------------------
    #随机二选一
    a = random.random()
    if a > 0.5:
    
        # 四个挂载点
        # add the first body 
        #需要同步修改search.py 45行
        R = apply_rule(rule=rules[0],input_graph=R,target_node_name='root')
        R = apply_rule(rule=rules[1],input_graph=R,target_node_name='body1')
        R = apply_rule(rule=rules[2],input_graph=R,target_node_name='body1')
        R = apply_rule(rule=rules[3],input_graph=R,target_node_name='body1')
        R = apply_rule(rule=rules[4],input_graph=R,target_node_name='body1')


    #--------------------------------------------------------------------------
    # 两个挂载点
    else:
        R = apply_rule(rule=rules[0],input_graph=R,target_node_name='root')
        R = apply_rule(rule=rules[5],input_graph=R,target_node_name='body1')
        R = apply_rule(rule=rules[6],input_graph=R,target_node_name='body1')



    #--------------------------------------------------------------------------
    # R = apply_rule(rule=rules[10],input_graph=R,target_node_name='body1')
    # R = apply_rule(rule=rules[12],input_graph=R,target_node_name='hand_mount1')
    # R = apply_rule(rule=rules[13],input_graph=R,target_node_name='hand_link1')
    # R = apply_rule(rule=rules[14],input_graph=R,target_node_name='hand_link_21')
    # R = apply_rule(rule=rules[15],input_graph=R,target_node_name='hand_link_21')
    return R