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
                        lhs_nodes={'root':{'require_label':'root','shape':'box','radius':'0.15 0.15 0.02','density':1000.0, 'body_pos':[0,0,0.82], 'geom_pos':[-0.02,0,0.07],'euler':[90,0,0],'label':'root'}},
                        lhs_edges=[],
                        rhs_nodes={'body':{'shape':'box','radius':'0.4 0.8 0.1','density':1000.0,'geom_euler':[0,0,0], 'geom_pos':[-0.02,0,0],'label':'body'},'root':{'label':'root'}},
                        rhs_edges=[{'from_node':'root','to_node':'body','range':[-5,5],'axis':[0,0,1]}])
    rules.append(rule)

    # rule1-1 1 右前
    rule = create_rule(name='make_body_with_limbmount_1',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.42,0.4,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount'}])
    rules.append(rule)
    
    # rule1-2 2 左前
    rule = create_rule(name='make_body_with_limbmount_2',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.45,0.4,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount'},])
    rules.append(rule)
    
    # rule1-3 3 
    rule = create_rule(name='make_body_with_limbmount_3',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.45,-0.4,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount'},])
    rules.append(rule)

    # rule1-4 4 右后
    rule = create_rule(name='make_body_with_limbmount_4',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.42,-0.4,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount'},])
    rules.append(rule)
    
    # rule5 在motor上加一个link
    rule = create_rule(name='append_limblink',
                        lhs_nodes={'motor':{'require_label':'motor'}},
                        lhs_edges=[],
                        rhs_nodes={'limblink':{'label':'limblink','shape':'capsule','length':0.6,'radius':0.07, 'body_pos':[0.084,0,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'motor','to_node':'limblink','label':'mo-li','axis':[0,1,0],'range':[-45,45],}]
                        )
    rules.append(rule)


    # rule6 在motor上添加一个thin link
    rule = create_rule(name='append_thin_limblink',
                        lhs_nodes={'motor':{'require_label':'motor'}},
                        lhs_edges=[],
                        rhs_nodes={'limblink':{'label':'limblink','shape':'capsule','length':0.6,'radius':0.06, 'body_pos':[0.084,0,0],'euler':[0,90,0]}},
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
        rhs_nodes={'motor':{'label':'motor','shape':'cylinder','length':0.084,'radius':0.132, 'body_pos':[0,0.05,0],'euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'limbmount','to_node':'motor','label':'mount-motor','ctrlrange':[-1,1]}]


    )
    rules.append(rule)



    # rule8 在motor上连一个link
    # rule = create_rule(name='append_limblink',
    #                     lhs_nodes={'motor':{'require_label':'motor'}},
    #                     lhs_edges=[],
    #                     rhs_nodes={'limblink':{'label':'limblink','shape':'capsule','length':0.6,'radius':0.06, 'body_pos':[0.084,0,0],'euler':[0,90,0]}},
    #                     rhs_edges=[{'from_node':'motor','to_node':'limblink','label':'mo-li','axis':[0,1,0],'range':[-0.1,0.1],}]
    #                     )
    # rules.append(rule)


    # rule8 在motor上连short limblink

    rule = create_rule(name='append_short_limblink',
                        lhs_nodes={'motor':{'require_label':'motor'}},
                        lhs_edges=[],
                        rhs_nodes={'short_limblink':{'require_label':'short_limblink','label':'short_limblink','shape':'capsule','length':0.3,'radius':0.06, 'body_pos':[0.03,0,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'short_limbmount','to_node':'limblink','label':'mo-sh','axis':[0,1,0],'range':[-45,45]}]
                        )
    rules.append(rule)

    #rule9 在link/thinlink末端添加一个motor

    rule = create_rule(
        name='add_motor_link_end',
        lhs_nodes={'limblink':{'require_label':'limblink'}},
        lhs_edges=[],
        rhs_nodes={'motor_link_end':{'require_label':'motor_link_end','label':'motor_link_end','shape':'cylinder','length':0.084,'radius':0.122, 'body_pos':[0.6,0,0],'euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'limblink','to_node':'motor_link_end','label':'motor-end','ctrlrange':[-1,1]}]


    )
    rules.append(rule)


    # #rule 在shortlink末端添加一个motor

    # rule = create_rule(
    #     name='add_motor_link_end',
    #     lhs_nodes={'short_limblink':{'require_label':'short_limblink'}},
    #     lhs_edges=[],
    #     rhs_nodes={'motor_link_end':{'label':'motor_link_end','shape':'cylinder','length':0.084,'radius':0.122, 'body_pos':[0.,0,0],'euler':[0,-90,0]}},
    #     rhs_edges=[{'from_node':'short_limblink','to_node':'motor_link_end','label':'motor-shend','ctrlrange':[-1,1]}]


    # )
    # rules.append(rule)

    #rule10 在body上加一个手的底座

    rule = create_rule(
        name='add_hand_mount',
        lhs_nodes={'body':{'require_label':'body'}},
        lhs_edges=[],
        rhs_nodes={'hand_mount':{'require_label':'hand_mount','label':'hand_mount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.1175,0.6,0.2],'euler':[0,90,0]}},
        rhs_edges=[{'from_node':'body','to_node':'hand_mount','label':'hand_mount','ctrlrange':[-1,1],'range':[-180,180]}]


    )
    rules.append(rule)

    # #rule12 手的底座加连杆1

    # rule = create_rule(
    #     name='add_hand_mount_link',
    #     lhs_nodes={'hand_mount':{'require_label':'hand_mount'}},
    #     lhs_edges=[],
    #     rhs_nodes={'hand_link':{'shape':'capsule','length':0.11,'radius':0.05, 'body_pos':[0.0,0,0.11],'euler':[0,90,0]}},
    #     rhs_edges=[{'from_node':'hand_mount','to_node':'hand_link','label':'hand_link','ctrlrange':[-1,1],'range':[-89,89]}]


    # )
    # rules.append(rule)

    # #rule13 手的底座加连杆1+连杆2

    # rule = create_rule(
    #     name='add_hand_link',
    #     lhs_nodes={'hand_link':{'require_label':'hand_link'}},
    #     lhs_edges=[],
    #     rhs_nodes={'hand_link_2':{'shape':'capsule','length':0.6,'radius':0.05, 'body_pos':[0,0,0],'euler':[0,90,0]}},
    #     rhs_edges=[{'from_node':'hand_link','to_node':'hand_link_2','label':'hand_link_2','ctrlrange':[-1,1],'range':[-60,60]}]


    # )
    # rules.append(rule)

    # #rule14 手的底座加连杆1+连杆2+爪子1
    # rule = create_rule(
    #     name='add_hand_',
    #     lhs_nodes={'hand_link_2':{'require_label':'hand_link_2'}},
    #     lhs_edges=[],
    #     rhs_nodes={'hand_1':{'shape':'capsule','length':0.1,'radius':0.02, 'body_pos':[0.64,0,0],'euler':[0,0,0]}},
    #     rhs_edges=[{'from_node':'hand_link','to_node':'hand_1','label':'hand_1','ctrlrange':[-1,1],'axis':[0,0,1],'range':[-0.05,-0.01],'type':'slide','damping':'2.5', 'stiffness':'80'}]


    # )
    # rules.append(rule)


    # #rule15 手的底座加连杆1+连杆2+爪子2
    # rule = create_rule(
    #     name='add_hand_',
    #     lhs_nodes={'hand_link_2':{'require_label':'hand_link_2'}},
    #     lhs_edges=[],
    #     rhs_nodes={'hand_2':{'shape':'capsule','length':0.1,'radius':0.02, 'body_pos':[0.64,0,0],'euler':[0,0,0]}},
    #     rhs_edges=[{'from_node':'hand_link','to_node':'hand_2','label':'hand_2','ctrlrange':[-1,1],'axis':[0,0,1],'range':[0.01,0.05],'type':'slide','damping':'2.5', 'stiffness':'80'}]


    # )
    # rules.append(rule)

    #rule110轮子
    rule = create_rule(
        name='add_wheel_link_end',
        lhs_nodes={'limblink':{'require_label':'limblink'}},
        lhs_edges=[],
        rhs_nodes={'wheel_link_end':{'require_label':'wheel_link_end','label':'wheel_link_end','shape':'cylinder','length':0.08,'radius':0.12, 'body_pos':[0.6,0,0],'euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'limblink','to_node':'wheel_link_end','label':'motor-end','ctrlrange':[-1,1],'gear':'45'}]


    )
    rules.append(rule)

    return rules





def create_4leg_rules_v2():
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
                        lhs_nodes={'root':{'require_label':'root','shape':'box','radius':'0.15 0.15 0.02','density':5.0, 'body_pos':[0,0,2.5], 'geom_pos':[-0.02,0,0.07],'euler':[90,0,0],'label':'root'}},
                        lhs_edges=[],
                        rhs_nodes={'body':{'shape':'box','radius':'0.4 0.8 0.1','density':5.0,'geom_euler':[0,0,0], 'geom_pos':[-0.02,0,0],'label':'body'},'root':{'label':'root'}},
                        rhs_edges=[{'from_node':'root','to_node':'body','range':[-5,5],'axis':[0,0,1]}])
    rules.append(rule)

    # rule1-1 1 右前
    rule = create_rule(name='make_body_with_limbmount_1',
                        lhs_nodes={'body':{'require_label':'body','density':5.0}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.5,0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-2 2 左前
    rule = create_rule(name='make_body_with_limbmount_2',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.5,0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-3 3 
    rule = create_rule(name='make_body_with_limbmount_3',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.5,-0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)

    # rule1-4 4 右后
    rule = create_rule(name='make_body_with_limbmount_4',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.5,-0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    

    # rule5 upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule6 upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule7 lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.4,0,0],'euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule8 lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.4,0,0],'euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)



    #rule9轮子
    rule = create_rule(
        name='add_wheel_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'wheel_link_end':{'require_label':'wheel_link_end','label':'wheel_link_end','shape':'cylinder','length':0.08,'radius':0.12, 'body_pos':[0.4,0,-0.04],'euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'wheel_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45'}]


    )
    rules.append(rule)

    #rule10 foot
    rule = create_rule(
        name='add_foot_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'foot_link_end':{'require_label':'foot_link_end','label':'foot_link_end','shape':'sphere','radius':0.06, 'body_pos':[0.4,0,0],'euler':[0,0,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-5,5]}]


    )
    rules.append(rule)

    #rule11 foot-type1
    rule = create_rule(
        name='add_foot_1',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'foot_1':{'require_label':'foot_1','label':'foot_1','shape':'capsule','length':0.1,'radius':0.05,'body_pos':[0.4,0,0],'euler':[0,0,120]}},
        rhs_edges=[{'from_node':'lower_link_b','to_node':'foot_1','label':'foot1','ctrlrange':[-1,1],'gear':'45','range':[-25,25],'axis':[0,0,1]}]


    )
    rules.append(rule)
    #rule12 foot-type2
    rule = create_rule(
        name='add_foot_2',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'foot_2':{'require_label':'foot_2','label':'foot_2','shape':'capsule','length':0.1,'radius':0.05,'body_pos':[0.4,0,0],'euler':[0,0,-120]}},
        rhs_edges=[{'from_node':'lower_link_f','to_node':'foot_2','label':'foot2','ctrlrange':[-1,1],'gear':'45','range':[-25,25],'axis':[0,0,1]}]


    )
    rules.append(rule)

    return rules






def create_4leg_rules_v3():
    '''
    功能:通过调用`create_rule`创建多个指定的语法规则
    ---------------
    输入:无

    输出:规则列表 `rules` （类型为`list`）
    注意：若添加新规则 需要判断是否允许重复搜索该规则 若不允许 需要同步修改search.py 45行 apply_rule.py 410行
    缩小了机器人的比例
    '''  
    rules = [] 
    # rule0 battery
    rule = create_rule(name='make_robot',
                        lhs_nodes={'root':{'require_label':'root','shape':'box','radius':'0.15 0.15 0.02','density':5.0, 'body_pos':[0,0,1.5625], 'geom_pos':[-0.0125,0,0.04375],'euler':[90,0,0],'label':'root'}},
                        lhs_edges=[],
                        rhs_nodes={'body':{'shape':'box','radius':'0.25 0.5 0.04','density':5.0,'geom_euler':[0,0,0], 'geom_pos':[-0.0125,0,0],'label':'body'},'root':{'label':'root'}},
                        rhs_edges=[{'from_node':'root','to_node':'body','range':[-5,5],'axis':[0,0,1]}])
    rules.append(rule)

    # rule1-1 1 右前
    rule = create_rule(name='make_body_with_limbmount_1',
                        lhs_nodes={'body':{'require_label':'body','density':5.0}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0.28,0.35,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-2 2 左前
    rule = create_rule(name='make_body_with_limbmount_2',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[-0.3,0.35,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-3 3 
    rule = create_rule(name='make_body_with_limbmount_3',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[-0.3,-0.35,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)

    # rule1-4 4 右后
    rule = create_rule(name='make_body_with_limbmount_4',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0.28,-0.35,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    

    # rule5 upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.1875,'radius':0.04375, 'body_pos':[0.0625,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule6 upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.1875,'radius':0.04375, 'body_pos':[0.0625,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule7 lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.1875,'radius':0.04375, 'body_pos':[0.25,0,0],'euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule8 lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.1875,'radius':0.04375, 'body_pos':[0.25,0,0],'euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)



    #rule9轮子
    rule = create_rule(
        name='add_wheel_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'wheel_link_end':{'require_label':'wheel_link_end','label':'wheel_link_end','shape':'cylinder','length':0.05,'radius':0.075, 'body_pos':[0.25,0,-0.025],'euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'wheel_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45'}]


    )
    rules.append(rule)

    #rule10 foot sphere
    rule = create_rule(
        name='add_foot_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'foot_link_end':{'require_label':'foot_link_end','label':'foot_link_end','shape':'sphere','radius':0.0375, 'body_pos':[0.25,0,0],'euler':[0,0,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-5,5]}]


    )
    rules.append(rule)

    #rule11 foot-type1
    rule = create_rule(
        name='add_foot_1',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'foot_1':{'require_label':'foot_1','label':'foot_1','shape':'capsule','length':0.0625,'radius':0.03125,'body_pos':[0.25,0,0],'euler':[0,0,120]}},
        rhs_edges=[{'from_node':'lower_link_b','to_node':'foot_1','label':'foot1','ctrlrange':[-1,1],'gear':'45','range':[-25,25],'axis':[0,0,1]}]


    )
    rules.append(rule)
    #rule12 foot-type2
    rule = create_rule(
        name='add_foot_2',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'foot_2':{'require_label':'foot_2','label':'foot_2','shape':'capsule','length':0.0625,'radius':0.03125,'body_pos':[0.25,0,0],'euler':[0,0,-120]}},
        rhs_edges=[{'from_node':'lower_link_f','to_node':'foot_2','label':'foot2','ctrlrange':[-1,1],'gear':'45','range':[-25,25],'axis':[0,0,1]}]


    )
    rules.append(rule)

    #rule13 foot tiny
    rule = create_rule(
        name='add_tiny_foot_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'tiny_foot_link_end':{'require_label':'tiny_foot_link_end','label':'tiny_foot_link_end','shape':'sphere','radius':0.003, 'body_pos':[0.2,0,0],'euler':[0,0,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'tiny_foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-5,5]}]


    )
    rules.append(rule)

    #rule14 foot flat
    rule = create_rule(
        name='add_flat_foot_link_end',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'flat_foot_link_end':{'require_label':'flat_foot_link_end','label':'flat_foot_link_end','shape':'box','radius':'0.045 0.025 0.005','body_pos':[0.20,0.08,0],'euler':[90,0,150]}},
        rhs_edges=[{'from_node':'lower_link_b','to_node':'flat_foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,10],'axis':[0,1,0]}]


    )
    rules.append(rule)
    return rules




def create_4leg_rules_v4():
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
                        lhs_nodes={'root':{'require_label':'root','shape':'box','radius':'0.15 0.15 0.02','density':5.0, 'body_pos':[0,0,2.5], 'geom_pos':[-0.02,0,0.07],'euler':[90,0,0],'label':'root'}},
                        lhs_edges=[],
                        rhs_nodes={'body':{'shape':'box','radius':'0.4 0.8 0.1','density':5.0,'geom_euler':[0,0,0], 'geom_pos':[-0.02,0,0],'label':'body'},'root':{'label':'root'}},
                        rhs_edges=[{'from_node':'root','to_node':'body','range':[-5,5],'axis':[0,0,1]}])
    rules.append(rule)

    # rule1-1 1 右前
    rule = create_rule(name='make_body_with_limbmount_1',
                        lhs_nodes={'body':{'require_label':'body','density':5.0}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.5,0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-2 2 左前
    rule = create_rule(name='make_body_with_limbmount_2',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.5,0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-3 3 
    rule = create_rule(name='make_body_with_limbmount_3',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.5,-0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)

    # rule1-4 4 右后
    rule = create_rule(name='make_body_with_limbmount_4',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.5,-0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    

    # rule5 upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule6 upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule7 -1upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule8 -1upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule9 -2upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule10 -2upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule11 -3upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule12 -3upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule13 +1upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule14 +1upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule9 +2upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule10 +2upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule11 +3upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule12 +3upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule13 +4upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule14 +4upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule15 lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule16 lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)


    # rule17 -1lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule18 -1lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule19 -2lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule20 -2lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule21 -3lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule22 -3lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)


    # rule23 +1lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule24 +1lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule25 +2lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule26 +2lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule27 +3lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule28 +3lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule29 +4lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule30 +4lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    #rule31轮子
    rule = create_rule(
        name='add_wheel_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'wheel_link_end':{'require_label':'wheel_link_end','label':'wheel_link_end','shape':'cylinder','length':0.08,'radius':0.12, 'body_pos':'wheel-parent','euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'wheel_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45'}]


    )
    rules.append(rule)

    #rule32 foot
    rule = create_rule(
        name='add_foot_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'foot_link_end':{'require_label':'foot_link_end','label':'foot_link_end','shape':'sphere','radius':0.06, 'body_pos':'parent','euler':[0,0,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-5,5]}]


    )
    rules.append(rule)

    #rule33 foot-type1
    rule = create_rule(
        name='add_foot_1',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'foot_1':{'require_label':'foot_1','label':'foot_1','shape':'capsule','length':0.1,'radius':0.05,'body_pos':'parent','euler':[0,0,120]}},
        rhs_edges=[{'from_node':'lower_link_b','to_node':'foot_1','label':'foot1','ctrlrange':[-1,1],'gear':'45','range':[-25,25],'axis':[0,0,1]}]


    )
    rules.append(rule)
    #rule34 foot-type2
    rule = create_rule(
        name='add_foot_2',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'foot_2':{'require_label':'foot_2','label':'foot_2','shape':'capsule','length':0.1,'radius':0.05,'body_pos':'parent','euler':[0,0,-120]}},
        rhs_edges=[{'from_node':'lower_link_f','to_node':'foot_2','label':'foot2','ctrlrange':[-1,1],'gear':'45','range':[-25,25],'axis':[0,0,1]}]


    )
    rules.append(rule)
    
    #rule35 small-foot
    rule = create_rule(
        name='add_foot_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'foot_link_end':{'require_label':'foot_link_end','label':'foot_link_end','shape':'sphere','radius':0.03, 'body_pos':'parent','euler':[0,0,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-5,5]}]


    )
    rules.append(rule)

    #rule36 foot flat
    rule = create_rule(
        name='add_flat_foot_link_end',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'flat_foot_link_end':{'require_label':'flat_foot_link_end','label':'flat_foot_link_end','shape':'box','radius':'0.045 0.045 0.005','body_pos':'flat-parent','euler':[90,0,150]}},
        rhs_edges=[{'from_node':'lower_link_b','to_node':'flat_foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,10],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule37 extra leg link yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule38 extra leg link yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule39 extra leg link +1 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.20,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule40 extra leg link +1 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.20,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule41 extra leg link +2 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link +2 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)


    #rule41 extra leg link +3 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link +3 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)


    #rule39 extra leg link -1 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.10,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule40 extra leg link -1 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.10,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule41 extra leg link -2 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.08,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link -2 yaw
    rule = create_rule( 
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.08,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)


    #rule41 extra leg link -3 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.06,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link -3 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.06,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)


    #rule37 extra leg link pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule38 extra leg link pitch
    rule = create_rule( 
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule39 extra leg link +1 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.20,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule40 extra leg link +1 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.20,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule41 extra leg link +2 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule42 extra leg link +2 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)


    #rule41 extra leg link +3 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule42 extra leg link +3 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)


    #rule39 extra leg link -1 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.10,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule40 extra leg link -1 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.10,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule41 extra leg link -2 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.08,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule42 extra leg link -2 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.08,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)


    #rule41 extra leg link -3 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.06,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule42 extra leg link -3 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.06,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    # rule5 upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule6 upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule7 -1upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule8 -1upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule9 -2upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule10 -2upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule11 -3upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule12 -3upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule13 +1upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule14 +1upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule9 +2upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule10 +2upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule11 +3upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule12 +3upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule13 +4upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule14 +4upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule15 lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule16 lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)


    # rule17 -1lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule18 -1lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule19 -2lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule20 -2lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule21 -3lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule22 -3lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)


    # rule23 +1lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule24 +1lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule25 +2lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule26 +2lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule27 +3lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule28 +3lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule29 +4lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule30 +4lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,1,0],'range':[-45,45],'gear':'45'}]
    )

        # rule5 upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule6 upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule7 -1upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule8 -1upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule9 -2upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule10 -2upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule11 -3upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule12 -3upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule13 +1upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule14 +1upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule9 +2upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule10 +2upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule11 +3upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule12 +3upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule13 +4upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule14 +4upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule15 lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule16 lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)


    # rule17 -1lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule18 -1lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule19 -2lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule20 -2lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule21 -3lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule22 -3lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)


    # rule23 +1lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule24 +1lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule25 +2lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule26 +2lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule27 +3lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule28 +3lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule29 +4lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule30 +4lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[1,0,0],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)
    
    return rules


def create_4leg_rules_v5():
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
                        lhs_nodes={'root':{'require_label':'root','shape':'box','radius':'0.15 0.15 0.02','density':5.0, 'body_pos':[0,0,2.5], 'geom_pos':[-0.02,0,0.07],'euler':[90,0,0],'label':'root'}},
                        lhs_edges=[],
                        rhs_nodes={'body':{'shape':'box','radius':'0.4 0.8 0.1','density':5.0,'geom_euler':[0,0,0], 'geom_pos':[-0.02,0,0],'label':'body'},'root':{'label':'root'}},
                        rhs_edges=[{'from_node':'root','to_node':'body','range':[-5,5],'axis':[0,0,1]}])
    rules.append(rule)

    # rule1-1 1 右前
    rule = create_rule(name='make_body_with_limbmount_1',
                        lhs_nodes={'body':{'require_label':'body','density':5.0}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.5,0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-2 2 左前
    rule = create_rule(name='make_body_with_limbmount_2',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.5,0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-3 3 
    rule = create_rule(name='make_body_with_limbmount_3',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.5,-0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)

    # rule1-4 4 右后
    rule = create_rule(name='make_body_with_limbmount_4',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.5,-0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    

    # rule5 upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule6 upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule7 -1upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.295,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule8 -1upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.295,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule9 -2upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.28,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule10 -2upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.28,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule11 -3upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.275,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule12 -3upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.275,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule13 +1upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.305,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule14 +1upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.305,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule9 +2upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.31,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule10 +2upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.31,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule11 +3upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.315,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule12 +3upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.315,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule13 +4upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.32,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule14 +4upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.32,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule15 lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule16 lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)


    # rule17 -1lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.295,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule18 -1lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.295,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule19 -2lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.29,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule20 -2lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.29,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule21 -3lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.285,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule22 -3lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.285,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)


    # rule23 +1lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.305,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule24 +1lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.305,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule25 +2lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.31,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule26 +2lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.31,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule27 +3lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.315,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule28 +3lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.315,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule29 +4lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.32,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule30 +4lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.32,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    #rule31轮子
    rule = create_rule(
        name='add_wheel_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'wheel_link_end':{'require_label':'wheel_link_end','label':'wheel_link_end','shape':'cylinder','length':0.08,'radius':0.12, 'body_pos':'wheel-parent','euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'wheel_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45'}]


    )
    rules.append(rule)

    #rule32 foot
    rule = create_rule(
        name='add_foot_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'foot_link_end':{'require_label':'foot_link_end','label':'foot_link_end','shape':'sphere','radius':0.06, 'body_pos':'parent','euler':[0,0,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-5,5]}]


    )
    rules.append(rule)

    #rule33 foot-type1
    rule = create_rule(
        name='add_foot_1',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'foot_1':{'require_label':'foot_1','label':'foot_1','shape':'capsule','length':0.1,'radius':0.05,'body_pos':'parent','euler':[0,0,120]}},
        rhs_edges=[{'from_node':'lower_link_b','to_node':'foot_1','label':'foot1','ctrlrange':[-1,1],'gear':'45','range':[-25,25],'axis':[0,0,1]}]


    )
    rules.append(rule)
    #rule34 foot-type2
    rule = create_rule(
        name='add_foot_2',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'foot_2':{'require_label':'foot_2','label':'foot_2','shape':'capsule','length':0.1,'radius':0.05,'body_pos':'parent','euler':[0,0,-120]}},
        rhs_edges=[{'from_node':'lower_link_f','to_node':'foot_2','label':'foot2','ctrlrange':[-1,1],'gear':'45','range':[-25,25],'axis':[0,0,1]}]


    )
    rules.append(rule)
    
    #rule35 small-foot
    rule = create_rule(
        name='add_foot_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'foot_link_end':{'require_label':'foot_link_end','label':'foot_link_end','shape':'sphere','radius':0.03, 'body_pos':'parent','euler':[0,0,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-5,5]}]


    )
    rules.append(rule)

    #rule14 foot flat
    rule = create_rule(
        name='add_flat_foot_link_end',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'flat_foot_link_end':{'require_label':'flat_foot_link_end','label':'flat_foot_link_end','shape':'box','radius':'0.045 0.045 0.005','body_pos':'flat-parent','euler':[90,0,150]}},
        rhs_edges=[{'from_node':'lower_link_b','to_node':'flat_foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,10],'axis':[0,1,0]}]
    )
    rules.append(rule)
    return rules


def create_4leg_rules_v8():
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
                        lhs_nodes={'root':{'require_label':'root','shape':'box','radius':'0.15 0.15 0.02','density':5.0, 'body_pos':[0,0,2.5], 'geom_pos':[-0.02,0,0.07],'euler':[90,0,0],'label':'root'}},
                        lhs_edges=[],
                        rhs_nodes={'body':{'shape':'box','radius':'0.4 0.8 0.1','density':5.0,'geom_euler':[0,0,0], 'geom_pos':[-0.02,0,0],'label':'body'},'root':{'label':'root'}},
                        rhs_edges=[{'from_node':'root','to_node':'body','range':[-5,5],'axis':[0,0,1]}])
    rules.append(rule)

    # rule1-1 1 右前
    rule = create_rule(name='make_body_with_limbmount_1',
                        lhs_nodes={'body':{'require_label':'body','density':5.0}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.5,0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-2 2 左前
    rule = create_rule(name='make_body_with_limbmount_2',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.5,0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-3 3 
    rule = create_rule(name='make_body_with_limbmount_3',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.5,-0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)

    # rule1-4 4 右后
    rule = create_rule(name='make_body_with_limbmount_4',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.5,-0.5,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    ## 2 legs
    # rule1-1 5 右前
    rule = create_rule(name='make_body_with_limbmount_1',
                        lhs_nodes={'body':{'require_label':'body','density':5.0}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[0.5,0,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)
    
    # rule1-2 6 左前
    rule = create_rule(name='make_body_with_limbmount_2',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'label':'limbmount','shape':'capsule','length':0.05,'radius':0.05, 'body_pos':[-0.5,0,0],'euler':[0,90,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','axis':[0,1,0],'label':'body-mount','range':[-5,5],'gear':'45'}])
    rules.append(rule)

    # rule5 upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule6 upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule7 -1upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule8 -1upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule9 -2upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule10 -2upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule11 -3upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule12 -3upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule13 +1upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule14 +1upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule9 +2upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule10 +2upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule11 +3upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule12 +3upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule13 +4upper_link_b
    rule = create_rule(name='make_upper_link_b',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_b':{'require_label':'upper_link_b','label':'upper_link_b','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,-45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_b','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}])
    rules.append(rule)

    # rule14 +4upper_link_f
    rule = create_rule(name='make_upper_link_f',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'upper_link_f':{'require_label':'upper_link_f','label':'upper_link_f','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':[0.1,0,0],'euler':[0,0,45]}},#'euler' need test
                        rhs_edges=[{'from_node':'limbmount','to_node':'upper_link_f','label':'mount-upper','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule15 lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule16 lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)


    # rule17 -1lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule18 -1lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule19 -2lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule20 -2lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.2,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule21 -3lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule22 -3lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)


    # rule23 +1lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule24 +1lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule25 +2lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule26 +2lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.4,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule27 +3lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule28 +3lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule29 +4lower_link_b
    rule = create_rule(name='make_lower_link_b',
                        lhs_nodes={'upper_link_f':{'require_label':'upper_link_f'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_b':{'require_label':'lower_link_b','label':'lower_link_b','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':'parent','euler':[0,0,-100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_f','to_node':'lower_link_b','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    # rule30 +4lower_link_f
    rule = create_rule(name='make_lower_link_f',
                        lhs_nodes={'upper_link_b':{'require_label':'upper_link_b'}},
                        lhs_edges=[],
                        rhs_nodes={'lower_link_f':{'require_label':'lower_link_f','label':'lower_link_f','shape':'capsule','length':0.5,'radius':0.07, 'body_pos':'parent','euler':[0,0,100]}},#'euler' need test
                        rhs_edges=[{'from_node':'upper_link_b','to_node':'lower_link_f','label':'upper-lower','axis':[0,0,1],'range':[-45,45],'gear':'45'}]
    )
    rules.append(rule)

    #rule31轮子
    rule = create_rule(
        name='add_wheel_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'wheel_link_end':{'require_label':'wheel_link_end','label':'wheel_link_end','shape':'cylinder','length':0.08,'radius':0.12, 'body_pos':'wheel-parent','euler':[0,-90,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'wheel_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45'}]


    )
    rules.append(rule)

    #rule32 foot
    rule = create_rule(
        name='add_foot_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'foot_link_end':{'require_label':'foot_link_end','label':'foot_link_end','shape':'sphere','radius':0.06, 'body_pos':'parent','euler':[0,0,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-5,5]}]


    )
    rules.append(rule)

    #rule33 foot-type1
    rule = create_rule(
        name='add_foot_1',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'foot_1':{'require_label':'foot_1','label':'foot_1','shape':'capsule','length':0.1,'radius':0.05,'body_pos':'parent','euler':[0,0,120]}},
        rhs_edges=[{'from_node':'lower_link_b','to_node':'foot_1','label':'foot1','ctrlrange':[-1,1],'gear':'45','range':[-25,25],'axis':[0,0,1]}]


    )
    rules.append(rule)
    #rule34 foot-type2
    rule = create_rule(
        name='add_foot_2',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'foot_2':{'require_label':'foot_2','label':'foot_2','shape':'capsule','length':0.1,'radius':0.05,'body_pos':'parent','euler':[0,0,-120]}},
        rhs_edges=[{'from_node':'lower_link_f','to_node':'foot_2','label':'foot2','ctrlrange':[-1,1],'gear':'45','range':[-25,25],'axis':[0,0,1]}]


    )
    rules.append(rule)
    
    #rule35 small-foot
    rule = create_rule(
        name='add_foot_link_end',
        lhs_nodes={'lower_link':{'require_label':'lower_link'}},
        lhs_edges=[],
        rhs_nodes={'foot_link_end':{'require_label':'foot_link_end','label':'foot_link_end','shape':'sphere','radius':0.03, 'body_pos':'parent','euler':[0,0,0]}},
        rhs_edges=[{'from_node':'lower_link','to_node':'foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-5,5]}]


    )
    rules.append(rule)

    #rule36 foot flat
    rule = create_rule(
        name='add_flat_foot_link_end',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'flat_foot_link_end':{'require_label':'flat_foot_link_end','label':'flat_foot_link_end','shape':'box','radius':'0.045 0.045 0.005','body_pos':'flat-parent','euler':[90,0,150]}},
        rhs_edges=[{'from_node':'lower_link_b','to_node':'flat_foot_link_end','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,10],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule37 extra leg link yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule38 extra leg link yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule39 extra leg link +1 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule40 extra leg link +1 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule41 extra leg link +2 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.40,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link +2 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.40,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)


    #rule41 extra leg link +3 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link +3 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)


    #rule39 extra leg link -1 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule40 extra leg link -1 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule41 extra leg link -2 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.20,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link -2 yaw
    rule = create_rule( 
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.20,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)


    #rule41 extra leg link -3 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link -3 yaw
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,1,0]}]
    )
    rules.append(rule)


    #rule37 extra leg link pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule38 extra leg link pitch
    rule = create_rule( 
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule39 extra leg link +1 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule40 extra leg link +1 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule41 extra leg link +2 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.40,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule42 extra leg link +2 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.40,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)


    #rule41 extra leg link +3 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule42 extra leg link +3 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)


    #rule39 extra leg link -1 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule40 extra leg link -1 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule41 extra leg link -2 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.20,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule42 extra leg link -2 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.20,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)


    #rule41 extra leg link -3 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)

    #rule42 extra leg link -3 pitch
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[0,0,1]}]
    )
    rules.append(rule)


##
        #rule38 extra leg link roll
    rule = create_rule( 
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.3,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)

    #rule39 extra leg link +1 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)

    #rule40 extra leg link +1 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.35,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)

    #rule41 extra leg link +2 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.40,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link +2 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.40,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)


    #rule41 extra leg link +3 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link +3 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.45,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)


    #rule39 extra leg link -1 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)

    #rule40 extra leg link -1 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.25,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)

    #rule41 extra leg link -2 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.20,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link -2 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.20,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)


    #rule41 extra leg link -3 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_b':{'require_label':'lower_link_b'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
    )
    rules.append(rule)

    #rule42 extra leg link -3 roll
    rule = create_rule(
        name='add_extra_leg_link',
        lhs_nodes={'lower_link_f':{'require_label':'lower_link_f'}},
        lhs_edges=[],
        rhs_nodes={'lower_link':{'require_label':'lower_link','label':'lower_link','shape':'capsule','length':0.15,'radius':0.07, 'body_pos':'parent','euler':[0,0,0]}},#'euler' need test
        rhs_edges=[{'from_node':'lower_link_b','to_node':'lower_link','label':'link-end','ctrlrange':[-1,1],'gear':'45','range':[-45,45],'axis':[1,0,0]}]
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