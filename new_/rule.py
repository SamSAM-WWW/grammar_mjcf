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

def create_rules():
    '''
    功能:通过调用`create_rule`创建多个指定的语法规则
    ---------------
    输入:无

    输出:规则列表 `rules` （类型为`list`）
    '''  
    rules = [] 
    # rule0
    rule = create_rule(name='make_robot',
                        lhs_nodes={'root':{'require_label':'root'}},
                        lhs_edges=[],
                        rhs_nodes={'body':{'label':'body'}},
                        rhs_edges=[{'from_node':'root','to_node':'body'}])
    rules.append(rule)

    # rule1
    rule = create_rule(name='make_body_with_limbmount',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'body':{'shape':'cylinder','length':0.1,'radius':0.5,'density':3.0},'limbmount':{'shape':'capsule','length':0.025,'radius':0.025}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge','offset':'0.3','axis_angle':'0 1 0 90'},])
    rules.append(rule)

    # rule2
    rule = create_rule(name='append_limblink',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'limblink':{'label':'limblink'}},
                        rhs_edges=[{'from_node':'limbmount','to_node':'limblink','label':'limb_joint'}]
                        )
    rules.append(rule)

    # rule3
    rule = create_rule(name='make_normal_limblink',
                        lhs_nodes={'limblink':{'require_label':'limblink'}},
                        lhs_edges=[],
                        rhs_nodes={'limblink':{'shape':'capsule','length':0.1,'radius':0.025}},
                        rhs_edges=[])
    rules.append(rule)

    # rule4
    rule = create_rule(name='make_left_roll_limb_joint',
                        lhs_nodes={},
                        lhs_edges=[{'from_node':'parent','to_node':'child','require_label':'limb_joint'}],
                        rhs_nodes={},
                        rhs_edges=[{'from_node':'parent','to_node':'child','type':'hinge','axis_angel':'0 1 0 -90','joint_axis':'1 0 0'}]
                        )
    rules.append(rule)




    return rules



def create_6leg_rules():
    '''
    功能:通过调用`create_rule`创建多个指定的语法规则
    ---------------
    输入:无

    输出:规则列表 `rules` （类型为`list`）
    '''  
    rules = [] 
    # rule0
    rule = create_rule(name='make_robot',
                        lhs_nodes={'root':{'require_label':'root','shape':'sphere','radius':0.0005,'density':3.0, 'body_pos':[0,0,2], 'geom_pos':[0,0,2]}},
                        lhs_edges=[],
                        rhs_nodes={'body':{'shape':'cylinder','length':0.1,'radius':0.5,'density':3.0,'euler':[0,90,0]},'root':{'label':'root'}},
                        rhs_edges=[{'from_node':'root','to_node':'body'}])
    rules.append(rule)

    # rule1-1 1
    rule = create_rule(name='make_body_with_limbmount_1',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,0.5,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
    rules.append(rule)
    
    # rule1-2 2
    rule = create_rule(name='make_body_with_limbmount_2',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,0.25,0.433]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
    rules.append(rule)
    
    # rule1-3 3
    rule = create_rule(name='make_body_with_limbmount_3',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,-0.25,0.433]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
    rules.append(rule)

    # rule1-4 4
    rule = create_rule(name='make_body_with_limbmount_4',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,-0.5,0]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
    rules.append(rule)
    
    # rule1-5 5
    rule = create_rule(name='make_body_with_limbmount_5',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,-0.25,-0.433]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
    rules.append(rule)
    
    # rule1-6 6
    rule = create_rule(name='make_body_with_limbmount_6',
                        lhs_nodes={'body':{'require_label':'body'}},
                        lhs_edges=[],
                        rhs_nodes={'limbmount':{'shape':'capsule','length':0.025,'radius':0.025, 'body_pos':[0,0.25,-0.433]}},
                        rhs_edges=[{'from_node':'body','to_node':'limbmount','type':'hinge'},])
    rules.append(rule)



    # rule7
    rule = create_rule(name='append_limblink',
                        lhs_nodes={'limbmount':{'require_label':'limbmount'}},
                        lhs_edges=[],
                        rhs_nodes={'limblink':{'label':'limblink','shape':'capsule','length':0.5,'radius':0.025, 'body_pos':[0,0,0]}},
                        rhs_edges=[{'from_node':'limbmount','to_node':'limblink','label':'limb_joint','axis':[0,1,0]}]
                        )
    rules.append(rule)

    return rules




rules = create_6leg_rules()
for rule in rules:
    print("================================")
    print("rule.name",rule.name)
    print("rule.lhs_nodes",rule.lhs_nodes)
    print("rule.lhs_edges",rule.lhs_edges)
    print("rule.rhs_nodes",rule.rhs_nodes)
    print("rule.rhs_edges",rule.rhs_edges)
    print("rule.common_nodes",rule.common_nodes)
    print("rule.common_edges",rule.common_edges)
    print("================================")