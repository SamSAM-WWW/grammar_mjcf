class Rule():
    def __init__(self):
        self.name = str
        self.lhs_nodes = {}
        self.lhs_edges = []
        self.rhs_nodes = {}
        self.rhs_edges = []
        self.common_nodes = {}
        self.common_edges = []

def create_rule(name:str, lhs_nodes:dict, lhs_edges:dict, rhs_nodes:dict, rhs_edges:dict):
    '''
    功能:创建一个语法规则
    ---------------
    输入:规则的名字`name` 左侧节点`lhs_node` 左侧边`lhs_edge` 右侧节点`rhs_node` 右侧边`rhs_edge`

    输出:一个规则 `rule` （类型为`Rule`）
    '''
    rule = Rule()
    rule.name = name
    rule.lhs_nodes = lhs_nodes
    rule.lhs_edges = lhs_edges
    rule.rhs_nodes = rhs_nodes
    rule.rhs_edges = rhs_edges

    # 处理 common_nodes
    common_keys = set(lhs_nodes.keys()) & set(rhs_nodes.keys())
    # 将相同键的信息合并
    for key in common_keys:
        rule.common_nodes[key] = {**lhs_nodes[key], **rhs_nodes[key]}


    # 处理 common_edges
    common_edges = []
    if lhs_edges is not None and rhs_edges is not None:
        for lhs_edge in lhs_edges:
            for rhs_edge in rhs_edges:
                if lhs_edge.get('from_node') == rhs_edge.get('from_node') and lhs_edge.get('to_node') == rhs_edge.get('to_node'):
                    common_edges.append({**lhs_edge, **rhs_edge})

    rule.common_edges = common_edges
    return rule

# def create_rules():
#     '''
#     功能:通过调用`create_rule`创建多个指定的语法规则
#     ---------------
#     输入:无

#     输出:规则列表 `rules` （类型为`list`）
#     '''  
#     rules = [] 
#     # rule0
#     rule = create_rule(name='make_robot',
#                         lhs_nodes={'root':{'require_label':'root'}},
#                         lhs_edges=[],
#                         rhs_nodes={'body':{'label':'body'}},
#                         rhs_edges=[{'from_node':'root','to_node':'body'}])
#     rules.append(rule)

#     # rule1
#     rule = create_rule(name='make_body_with_limbmount',
#                         lhs_nodes={'body':{'require_label':'body'}},
#                         lhs_edges=[],
#                         rhs_nodes={'body':{'shape':'cylinder','length':0.1,'radius':0.5,'density':3.0},'limbmount':{'shape':'capsule','length':0.025,'radius':0.025}},
#                         rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','offset':'0.3'},])
#     rules.append(rule)

#     # rule2
#     rule = create_rule(name='append_limblink',
#                         lhs_nodes={'limbmount':{'require_label':'limbmount'}},
#                         lhs_edges=[],
#                         rhs_nodes={'limblink':{'label':'limblink'}},
#                         rhs_edges=[{'from_node':'limbmount','to_node':'limblink','label':'limb_joint'}]
#                         )
#     rules.append(rule)

#     # rule3
#     rule = create_rule(name='make_normal_limblink',
#                         lhs_nodes={'limblink':{'require_label':'limblink'}},
#                         lhs_edges=[],
#                         rhs_nodes={'limblink':{'shape':'capsule','length':0.1,'radius':0.025}},
#                         rhs_edges=[])
#     rules.append(rule)

#     # rule4
#     rule = create_rule(name='make_left_roll_limb_joint',
#                         lhs_nodes={},
#                         lhs_edges=[{'from_node':'parent','to_node':'child','require_label':'limb_joint'}],
#                         rhs_nodes={},
#                         rhs_edges=[{'from_node':'parent','to_node':'child','type':'hinge','joint_axis':'1 0 0'}]
#                         )
#     rules.append(rule)




#     return rules



# def create_6leg_rules():
#     '''
#     功能:通过调用`create_rule`创建多个指定的语法规则
#     ---------------
#     输入:无

#     输出:规则列表 `rules` （类型为`list`）
#     '''  
#     rules = [] 
#     # rule0
#     rule = create_rule(name='make_robot',
#                         lhs_nodes={'root':{'require_label':'root','shape':'sphere','radius':0.0005,'density':3.0, 'body_pos':[0,0,2], 'geom_pos':[0,0,2]}},
#                         lhs_edges=[],
#                         rhs_nodes={'body':{'shape':'box','radius':'0.203 0.4282 0.05','density':3.0,'euler':[0,90,0],'geom_euler':[0,90,0]},'root':{'label':'root'}},
#                         rhs_edges=[{'from_node':'root','to_node':'body'}])
#     rules.append(rule)

#     # rule1-1 1 右前
#     rule = create_rule(name='make_body_with_limbmount_1',
#                         lhs_nodes={'body':{'require_label':'body'}},
#                         lhs_edges=[],
#                         rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,0.5,0]}},
#                         rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
#     rules.append(rule)
    
#     # rule1-2 2 左前
#     rule = create_rule(name='make_body_with_limbmount_2',
#                         lhs_nodes={'body':{'require_label':'body'}},
#                         lhs_edges=[],
#                         rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,0.25,0.433]}},
#                         rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
#     rules.append(rule)
    
#     # rule1-3 3 左后
#     rule = create_rule(name='make_body_with_limbmount_3',
#                         lhs_nodes={'body':{'require_label':'body'}},
#                         lhs_edges=[],
#                         rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,-0.25,0.433]}},
#                         rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
#     rules.append(rule)

#     # rule1-4 4 右后
#     rule = create_rule(name='make_body_with_limbmount_4',
#                         lhs_nodes={'body':{'require_label':'body'}},
#                         lhs_edges=[],
#                         rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,-0.5,0]}},
#                         rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
#     rules.append(rule)
    
#     # rule1-5 5
#     rule = create_rule(name='make_body_with_limbmount_5',
#                         lhs_nodes={'body':{'require_label':'body'}},
#                         lhs_edges=[],
#                         rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,-0.25,-0.433]}},
#                         rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
#     rules.append(rule)
    
#     # rule1-6 6
#     rule = create_rule(name='make_body_with_limbmount_6',
#                         lhs_nodes={'body':{'require_label':'body'}},
#                         lhs_edges=[],
#                         rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,0.25,-0.433]}},
#                         rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
#     rules.append(rule)



#     # rule7
#     rule = create_rule(name='append_limblink',
#                         lhs_nodes={'limbmount':{'require_label':'limbmount'}},
#                         lhs_edges=[],
#                         rhs_nodes={'limblink':{'label':'limblink','shape':'capsule','length':0.6,'radius':0.06, 'body_pos':[0,0,0]}},
#                         rhs_edges=[{'from_node':'limbmount','to_node':'limblink','label':'limb_joint','axis':[0,1,0]}]
#                         )
#     rules.append(rule)


#     # rule8
#     rule = create_rule(name='append_thin_limblink',
#                         lhs_nodes={'limbmount':{'require_label':'limbmount'}},
#                         lhs_edges=[],
#                         rhs_nodes={'limblink':{'label':'limblink','shape':'capsule','length':0.6,'radius':0.03, 'body_pos':[0,0,0]}},
#                         rhs_edges=[{'from_node':'limbmount','to_node':'limblink','label':'limb_joint','axis':[0,1,0]}]
#                         )
#     rules.append(rule)

# # rule9
#     rule = create_rule(name='add_spring_leg',
#                         lhs_nodes={'limblink':{'require_label':'limblink'}},
#                         lhs_edges=[],
#                         rhs_nodes={'leg':{'label':'leg','shape':'capsule','length':0.8,'radius':0.08, 'body_pos':[0.6,0,0]}},
#                         rhs_edges=[{'from_node':'limblink','to_node':'leg','label':'spring','axis':[1,0,0],'type':'slide', 'stiffness':'80','damping':'2.5','range':[-0.1,0.1]}]
#                         )
#     rules.append(rule)



# # rule10 基于现实物理约束
#     rule = create_rule(
#         name='add_motor',
#         lhs_nodes={'limbmount':{'require_label':'limbmount'}},
#         lhs_edges=[],
#         rhs_nodes={'motor':{'label':'motor','shape':'cylinder','length':0.042,'radius':0.066, 'body_pos':[0,0,0]}},
#         rhs_edges=[{'from_node':'limbmount','to_node':'motor','label':'motor'}]


#     )
#     rules.append(rule)


#     return rules

def create_4leg_rules():
    '''
    功能:通过调用`create_rule`创建多个指定的语法规则
    ---------------
    输入:无

    输出:规则列表 `rules` （类型为`list`）
    注意：若添加新规则 需要判断是否允许重复搜索该规则 若不允许 需要同步修改search.py 45行 apply_rule.py 410行
    '''  
    rules = [] 
    # rule0 battery
    rule = create_rule(name='make_robot',
                        lhs_nodes={'root':{'require_label':'root','shape':'box','radius':'0.2 0.2 0.02','density':3.0, 'body_pos':[0,0,2], 'geom_pos':[-0.002,0,0.02]}},
                        lhs_edges=[],
                        rhs_nodes={'body':{'shape':'box','radius':'0.2 0.4 0.05','density':3.0,'euler':[0,0,0],'geom_euler':[0,0,0], 'geom_pos':[-0.02,0,0]},'root':{'label':'root'}},
                        rhs_edges=[{'from_node':'root','to_node':'body','range':[-45,45]}])
    rules.append(rule)

    # rule1-1 1 右前
    rule = create_rule(name='make_body_with_limbmount_1',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0.1875,0.2,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount'}])
    rules.append(rule)
    
    # rule1-2 2 左前
    rule = create_rule(name='make_body_with_limbmount_2',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[-0.225,0.2,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount'},])
    rules.append(rule)
    
    # rule1-3 3 右后
    rule = create_rule(name='make_body_with_limbmount_3',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[-0.225,-0.2,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount'},])
    rules.append(rule)

    # rule1-4 4 左后
    rule = create_rule(name='make_body_with_limbmount_4',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0.1875,-0.2,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount'},])
    rules.append(rule)
    
    # rule5 在motor上加一个link
    rule = create_rule(name='append_limblink',
                        lhs_nodes={'motor':{'require_label':'motor'}},
                        lhs_edges=[],
                        rhs_nodes={'limblink':{'label':'limblink','shape':'capsule','length':0.3,'radius':0.035, 'body_pos':[0.042,0,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'motor','to_node':'limblink','label':'mo-li','axis':[0,1,0],'range':[-45,45],}]
                        )
    rules.append(rule)


    # rule6 在motor上添加一个thin link
    rule = create_rule(name='append_thin_limblink',
                        lhs_nodes={'motor':{'require_label':'motor'}},
                        lhs_edges=[],
                        rhs_nodes={'limblink':{'label':'limblink','shape':'capsule','length':0.3,'radius':0.03, 'body_pos':[0.042,0,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'limbmount','to_node':'limblink','label':'mo-thin','axis':[0,1,0],'range':[-45,45]}]
                        )
    rules.append(rule)

# # rule7 在link的末尾添加一个弹簧腿
#     rule = create_rule(name='add_spring_leg',
#                         lhs_nodes={'limblink':{'require_label':'limblink'}},
#                         lhs_edges=[],
#                         rhs_nodes={'leg':{'label':'leg','shape':'capsule','length':0.8,'radius':0.08, 'body_pos':[0.6,0,0]}},
#                         rhs_edges=[{'from_node':'limblink','to_node':'leg','label':'spring','axis':[1,0,0],'type':'slide', 'stiffness':'80','damping':'2.5','range':[-0.1,0.1]}]
#                         )
#     rules.append(rule)



# rule7 在limbmount 添加一个motor
    rule = create_rule(
        name='add_motor',
        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
        lhs_edges=[],
        rhs_nodes={'motor':{'label':'motor','shape':'cylinder','length':0.042,'radius':0.066, 'body_pos':[0,0,0],'euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'limbmount','to_node':'motor','label':'mount-motor','ctrlrange':[-1,1]}]


    )
    rules.append(rule)



    # # rule9 在motor上连一个link
    # rule = create_rule(name='append_limblink',
    #                     lhs_nodes={'motor':{'require_label':'motor'}},
    #                     lhs_edges=[],
    #                     rhs_nodes={'limblink':{'label':'limblink','shape':'capsule','length':0.3,'radius':0.06, 'body_pos':[0,0,0],'euler':[0,90,0]}},
    #                     rhs_edges=[{'from_node':'motor','to_node':'limblink','label':'mo-li','axis':[0,1,0],'range':[-0.1,0.1],}]
    #                     )
    # rules.append(rule)


    # rule8 在motor上连short limblink

    rule = create_rule(name='append_short_limblink',
                        lhs_nodes={'motor':{'require_label':'motor'}},
                        lhs_edges=[],
                        rhs_nodes={'short_limblink':{'label':'short_limblink','shape':'capsule','length':0.15,'radius':0.03, 'body_pos':[0.015,0,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'short_limbmount','to_node':'limblink','label':'mo-sh','axis':[0,1,0],'range':[-45,45]}]
                        )
    rules.append(rule)

    #rule9 在link/thinlink末端添加一个motor

    rule = create_rule(
        name='add_motor_link_end',
        lhs_nodes={'limblink':{'require_label':'limblink'}},
        lhs_edges=[],
        rhs_nodes={'motor_link_end':{'label':'motor_link_end','shape':'cylinder','length':0.042,'radius':0.066, 'body_pos':[0.3,0,0],'euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'limblink','to_node':'motor_link_end','label':'motor-end','ctrlrange':[-1,1]}]


    )
    rules.append(rule)


    #rule10 在shortlink末端添加一个motor

    rule = create_rule(
        name='add_motor_link_end',
        lhs_nodes={'short_limblink':{'require_label':'short_limblink'}},
        lhs_edges=[],
        rhs_nodes={'motor_link_end':{'label':'motor_link_end','shape':'cylinder','length':0.042,'radius':0.066, 'body_pos':[0.15,0,0],'euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'short_limblink','to_node':'motor_link_end','label':'motor-shend','ctrlrange':[-1,1]}]


    )
    rules.append(rule)

    #rule11 在body上加一个手的底座

    rule = create_rule(
        name='add_hand_mount',
        lhs_nodes={'body':{'require_label':'body'}},
        lhs_edges=[],
        rhs_nodes={'hand_mount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[-0.05875,0.3,0.1],'euler':[0,90,0]}},
        rhs_edges=[{'from_node':'body','to_node':'hand_mount','label':'hand_mount','ctrlrange':[-1,1],'range':[-180,180]}]


    )
    rules.append(rule)

    #rule12 手的底座加连杆1

    rule = create_rule(
        name='add_hand_mount_link',
        lhs_nodes={'hand_mount':{'require_label':'hand_mount'}},
        lhs_edges=[],
        rhs_nodes={'hand_link':{'shape':'capsule','length':0.055,'radius':0.025, 'body_pos':[0.0,0,0.055],'euler':[0,90,0]}},
        rhs_edges=[{'from_node':'hand_mount','to_node':'hand_link','label':'hand_link','ctrlrange':[-1,1],'range':[-89,89]}]


    )
    rules.append(rule)

    #rule13 手的底座加连杆1+连杆2

    rule = create_rule(
        name='add_hand_link',
        lhs_nodes={'hand_link':{'require_label':'hand_link'}},
        lhs_edges=[],
        rhs_nodes={'hand_link_2':{'shape':'capsule','length':0.3,'radius':0.025, 'body_pos':[0,0,0],'euler':[0,90,0]}},
        rhs_edges=[{'from_node':'hand_link','to_node':'hand_link_2','label':'hand_link_2','ctrlrange':[-1,1],'range':[-60,60]}]


    )
    rules.append(rule)

    #rule14 手的底座加连杆1+连杆2+爪子1
    rule = create_rule(
        name='add_hand_',
        lhs_nodes={'hand_link_2':{'require_label':'hand_link_2'}},
        lhs_edges=[],
        rhs_nodes={'hand_1':{'shape':'capsule','length':0.05,'radius':0.01, 'body_pos':[0.32,0,0],'euler':[0,0,0]}},
        rhs_edges=[{'from_node':'hand_link','to_node':'hand_1','label':'hand_1','ctrlrange':[-1,1],'axis':[0,0,1],'range':[-0.05,-0.01],'type':'slide','damping':'2.5', 'stiffness':'80'}]


    )
    rules.append(rule)


    #rule15 手的底座加连杆1+连杆2+爪子2
    rule = create_rule(
        name='add_hand_',
        lhs_nodes={'hand_link_2':{'require_label':'hand_link_2'}},
        lhs_edges=[],
        rhs_nodes={'hand_2':{'shape':'capsule','length':0.05,'radius':0.01, 'body_pos':[0.32,0,0],'euler':[0,0,0]}},
        rhs_edges=[{'from_node':'hand_link','to_node':'hand_2','label':'hand_2','ctrlrange':[-1,1],'axis':[0,0,1],'range':[0.01,0.05],'type':'slide','damping':'2.5', 'stiffness':'80'}]


    )
    rules.append(rule)

    #rule16 轮子
    rule = create_rule(
        name='add_wheel_link_end',
        lhs_nodes={'limblink':{'require_label':'limblink'}},
        lhs_edges=[],
        rhs_nodes={'wheel_link_end':{'label':'wheel_link_end','shape':'cylinder','length':0.04,'radius':0.06, 'body_pos':[0.3,0,0],'euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'limblink','to_node':'wheel_link_end','label':'motor-end','ctrlrange':[-1,1],'gear':'45'}]


    )
    rules.append(rule)

    return rules


# rules = create_6leg_rules()
# for rule in rules:
#     print("================================")
#     print("rule.name",rule.name)
#     print("rule.lhs_nodes",rule.lhs_nodes)
#     print("rule.lhs_edges",rule.lhs_edges)
#     print("rule.rhs_nodes",rule.rhs_nodes)
#     print("rule.rhs_edges",rule.rhs_edges)
#     print("rule.common_nodes",rule.common_nodes)
#     print("rule.common_edges",rule.common_edges)
#     print("================================")