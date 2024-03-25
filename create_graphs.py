import networkx as nx


def my_graph():
    graphs = []
    subgraph_info = {}  # 存储左右子图信息的字典
    '''
    发现确实从dot文件读取难度巨大 通过直接在python代码中构建就简单很多

    return a list of all the graphs
    ----------
    '''
    ###########################################################################################################
    # 创建图0 边的属性必须写，如果是空必须写成{}，否则读取bug
    G0 = nx.DiGraph(name="make_robot")

    G0.add_node("robot", label="robot", type="hinge",joint_axis="1 0 0")
    G0.add_node("head", label="head", type="hinge",joint_axis="0 1 0")
    # for node in G0.nodes:
    #     node_data = G0.nodes[node]
    #     print("node info test")
    #     print(node_data['label'], node_data['type'], node_data['joint_axis'])
    
    # # 添加左子图及其节点和边
    # L_nodes_0 = ["robot"]
    # L_edges_0 = []

    # # 添加右子图及其节点和边
    # R_nodes_0 = ["head", "body", "tail"]
    # R_edges_0 = [("head", "body", {"label": "body_joint"}), ("body", "tail", {"label": "body_joint"})]

    # # 向根图添加左右两个子图
    # G0.add_nodes_from(L_nodes_0)
    # G0.add_nodes_from(R_nodes_0)
    # G0.add_edges_from(R_edges_0)

    # # 创建左子图
    # L_subgraph = G0.subgraph(L_nodes_0 + [n for u, v, _ in L_edges_0 for n in [u, v]]).copy()
    # # 添加左子图专属属性...

    # # 创建右子图
    # R_subgraph = G0.subgraph(R_nodes_0 + [n for u, v, _ in R_edges_0 for n in [u, v]]).copy()
    # # 添加右子图专属属性...

    # # store in graphs
    # graphs.append(G0)




    ###########################################################################################################
    # 创建图1 边的属性必须写，如果是空必须写成{}，否则读取bug
    G1 = nx.DiGraph(name="append_body")

    # 添加左子图及其节点和边
    L_nodes_1 = ["tail"]
    L_edges_1 = [("parent","tail",{"id": "parent_edges"})]

    # 添加右子图及其节点和边
    R_nodes_1 = ["tail", "body"]
    R_edges_1 = [("parent", "body", {"id": "parent_edges"}), ("body", "tail", {"label": "body_joint"})]

    # 向根图添加左右两个子图
    G1.add_nodes_from(L_nodes_1)
    G1.add_nodes_from(R_nodes_1)
    G1.add_edges_from(R_edges_1)

    # 创建左子图
    L_subgraph = G1.subgraph(L_nodes_1 + [n for u, v, _ in L_edges_1 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # 创建右子图
    R_subgraph = G1.subgraph(R_nodes_1 + [n for u, v, _ in R_edges_1 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G1.copy())


    ###########################################################################################################
    # 创建图2  边的属性必须写，如果是空必须写成{}，否则读取bug
    G2 = nx.DiGraph(name="make_body_with_legs")

    # 添加左子图及其节点和边
    L_nodes_2 = ["body"]
    L_edges_2 = []

    # 添加右子图及其节点和边
    R_nodes_2 = ["body", "limb_mount", "limb_link", "limb"]
    R_edges_2 = [("body", "limb_mount", {"type": "fixed", "offset":0.5, "axis_angle":"0 1 0 90"}),
                ("body", "limb_mount", {"type": "fixed", "offset":0.5, "axis_angle":"0 1 0 90", "mirror":True}), 
                ("limb_mount", "limb_link", {"label": "limb_joint"}), 
                ("limb_link","limb",{})]

    # 向根图添加左右两个子图
    G2.add_nodes_from(L_nodes_2)
    G2.add_nodes_from(R_nodes_2)
    G2.add_edges_from(R_edges_2)
    # 创建左子图
    L_subgraph = G2.subgraph(L_nodes_2 + [n for u, v, _ in L_edges_2 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G2.subgraph(R_nodes_2 + [n for u, v, _ in R_edges_2 for n in [u, v]]).copy()
    # 添加右子图专属属性...
    R_subgraph.nodes["body"].update(shape="capsule", length=0.15, radius=0.045, density=3.0)

    # store in graphs
    graphs.append(G2.copy())


    ###########################################################################################################
    # 创建图3
    G3 = nx.DiGraph(name="make_body_without_legs")

    # 添加左子图及其节点和边
    L_nodes_3 = ["body"]
    L_edges_3 = []

    # 添加右子图及其节点和边
    R_nodes_3 = [("body")]
    R_edges_3 = []

    # 向根图添加左右两个子图
    G3.add_nodes_from(L_nodes_3)
    G3.add_nodes_from(R_nodes_3)
    G3.add_edges_from(R_edges_3)

    # 创建左子图
    L_subgraph = G3.subgraph(L_nodes_3 + [n for u, v, _ in L_edges_3 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G3.subgraph(R_nodes_3 + [n for u, v, _ in R_edges_3 for n in [u, v]]).copy()
    # 添加右子图专属属性...
    R_subgraph.nodes["body"].update(shape="capsule", length=0.15, radius=0.045, density=3.0)

    # store in graphs
    graphs.append(G3.copy())



    ###########################################################################################################
    # 创建图4
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G4 = nx.DiGraph(name="append_limb_link")

    # 添加左子图及其节点和边
    L_nodes_4 = ["limb"]
    L_edges_4 = [("parent","limb",{})]

    # 添加右子图及其节点和边
    R_nodes_4 = ["limb","limb_link"]
    R_edges_4 = [("parent","limb_link",{"label":"limb_joint"}),("limb_link","limb",{})]

    # 向根图添加左右两个子图
    G4.add_nodes_from(L_nodes_4)
    G4.add_edges_from(L_edges_4)
    G4.add_nodes_from(R_nodes_4)
    G4.add_edges_from(R_edges_4)

    # 创建左子图
    L_subgraph = G4.subgraph(L_nodes_4 + [n for u, v, _ in L_edges_4 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G4.subgraph(R_nodes_4 + [n for u, v, _ in R_edges_4 for n in [u, v]]).copy()
    # 添加右子图专属属性...


    # store in graphs
    graphs.append(G4.copy())


    ###########################################################################################################
    # 创建图5
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="end_limb")

    # 添加左子图及其节点和边
    L_nodes_5 = ["limb"]
    L_edges_5 = [("parent","limb",{})]

    # 添加右子图及其节点和边
    R_nodes_5 = ["parent"]
    R_edges_5 = []

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_5)
    G.add_edges_from(L_edges_5)
    G.add_nodes_from(R_nodes_5)
    G.add_edges_from(R_edges_5)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_5 + [n for u, v, _ in L_edges_5 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_5 + [n for u, v, _ in R_edges_5 for n in [u, v]]).copy()
    # 添加右子图专属属性...


    # store in graphs
    graphs.append(G.copy())



    ###########################################################################################################
    # 创建图6
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="end_tail")

    # 添加左子图及其节点和边
    L_nodes_6 = ["tail"]
    L_edges_6 = [("parent","tail",{})]

    # 添加右子图及其节点和边
    R_nodes_6 = ["parent"]
    R_edges_6 = []

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_6)
    G.add_edges_from(L_edges_6)
    G.add_nodes_from(R_nodes_6)
    G.add_edges_from(R_edges_6)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_6 + [n for u, v, _ in L_edges_6 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_6 + [n for u, v, _ in R_edges_6 for n in [u, v]]).copy()
    # 添加右子图专属属性...


    # store in graphs
    graphs.append(G.copy())




    ###########################################################################################################
    # 创建图7
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="end_head").copy()

    # 添加左子图及其节点和边
    L_nodes_7 = ["head"]
    L_edges_7 = [("head","child",{})]

    # 添加右子图及其节点和边
    R_nodes_7 = ["child"]
    R_edges_7 = []

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_7)
    G.add_edges_from(L_edges_7)
    G.add_nodes_from(R_nodes_7)
    G.add_edges_from(R_edges_7)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_7 + [n for u, v, _ in L_edges_7 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_7 + [n for u, v, _ in R_edges_7 for n in [u, v]]).copy()
    # 添加右子图专属属性...


    # store in graphs
    graphs.append(G.copy())





    ###########################################################################################################
    # 创建图8
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_normal_limb_link")

    # 添加左子图及其节点和边
    L_nodes_8 = ["limb_link"]
    L_edges_8 = []

    # 添加右子图及其节点和边
    R_nodes_8 = ["limb_link"]
    R_edges_8 = []

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_8)
    G.add_edges_from(L_edges_8)
    G.add_nodes_from(R_nodes_8)
    G.add_edges_from(R_edges_8)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_8 + [n for u, v, _ in L_edges_8 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_8 + [n for u, v, _ in R_edges_8 for n in [u, v]]).copy()
    # 添加右子图专属属性...
    R_subgraph.nodes["limb_link"].update(shape="capsule", length=0.15, radius=0.025)

    # store in graphs
    graphs.append(G.copy())




    ###########################################################################################################
    # 创建图9
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_long_limb_link")

    # 添加左子图及其节点和边
    L_nodes_9 = ["limb_link"]
    L_edges_9 = []

    # 添加右子图及其节点和边
    R_nodes_9 = ["limb_link"]
    R_edges_9 = []

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_9)
    G.add_edges_from(L_edges_9)
    G.add_nodes_from(R_nodes_9)
    G.add_edges_from(R_edges_9)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_9 + [n for u, v, _ in L_edges_9 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_9 + [n for u, v, _ in R_edges_9 for n in [u, v]]).copy()
    # 添加右子图专属属性...
    R_subgraph.nodes["limb_link"].update(shape="capsule", length=0.15, radius=0.025)

    # store in graphs
    graphs.append(G.copy())


    ###########################################################################################################
    # 创建图10
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_fixed_body_joint")

    # 添加左子图及其节点和边
    L_nodes_10 = []
    L_edges_10 = [("parent", "child", {"require_label":"body_joint"})]

    # 添加右子图及其节点和边
    R_nodes_10 = []
    R_edges_10 = [("parent", "child", {"type":"fixed"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_10)
    G.add_edges_from(L_edges_10)
    G.add_nodes_from(R_nodes_10)
    G.add_edges_from(R_edges_10)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_10 + [n for u, v, _ in L_edges_10 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_10 + [n for u, v, _ in R_edges_10 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())



    ###########################################################################################################
    # 创建图11
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_roll_body_joint")

    # 添加左子图及其节点和边
    L_nodes_11 = []
    L_edges_11 = [("parent", "child", {"require_label":"body_joint"})]

    # 添加右子图及其节点和边
    R_nodes_11 = []
    R_edges_11 = [("parent", "child", {"type":"hinge", "joint_axis":"1 0 0"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_11)
    G.add_edges_from(L_edges_11)
    G.add_nodes_from(R_nodes_11)
    G.add_edges_from(R_edges_11)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_11 + [n for u, v, _ in L_edges_11 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_11 + [n for u, v, _ in R_edges_11 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())


    ###########################################################################################################
    # 创建图12
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_swing_body_joint")

    # 添加左子图及其节点和边
    L_nodes_12 = []
    L_edges_12 = [("parent", "child", {"require_label":"body_joint"})]

    # 添加右子图及其节点和边
    R_nodes_12 = []
    R_edges_12 = [("parent", "child", {"type":"hinge", "joint_axis":"0 1 0"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_12)
    G.add_edges_from(L_edges_12)
    G.add_nodes_from(R_nodes_12)
    G.add_edges_from(R_edges_12)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_12 + [n for u, v, _ in L_edges_12 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_12 + [n for u, v, _ in R_edges_12 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())


    ###########################################################################################################
    # 创建图13
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_lift_body_joint")

    # 添加左子图及其节点和边
    L_nodes_13 = []
    L_edges_13 = [("parent", "child", {"require_label":"body_joint"})]

    # 添加右子图及其节点和边
    R_nodes_13 = []
    R_edges_13 = [("parent", "child", {"type":"hinge", "joint_axis":"0 0 1"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_13)
    G.add_edges_from(L_edges_13)
    G.add_nodes_from(R_nodes_13)
    G.add_edges_from(R_edges_13)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_13 + [n for u, v, _ in L_edges_13 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_13 + [n for u, v, _ in R_edges_13 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())


    ###########################################################################################################
    # 创建图14
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_left_roll_limb_joint")

    # 添加左子图及其节点和边
    L_nodes_14 = []
    L_edges_14 = [("parent", "child", {"require_label":"limb_joint"})]

    # 添加右子图及其节点和边
    R_nodes_14 = []
    R_edges_14 = [("parent", "child", {"type":"hinge", "axis_angle":"0 1 0 -90", "joint_axis":"1 0 0"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_14)
    G.add_edges_from(L_edges_14)
    G.add_nodes_from(R_nodes_14)
    G.add_edges_from(R_edges_14)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_14 + [n for u, v, _ in L_edges_14 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_14 + [n for u, v, _ in R_edges_14 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())



    ###########################################################################################################
    # 创建图15
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_right_roll_limb_joint")

    # 添加左子图及其节点和边
    L_nodes_15 = []
    L_edges_15 = [("parent", "child", {"require_label":"limb_joint"})]

    # 添加右子图及其节点和边
    R_nodes_15 = []
    R_edges_15 = [("parent", "child", {"type":"hinge", "axis_angle":"0 1 0 90", "joint_axis":"1 0 0"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_15)
    G.add_edges_from(L_edges_15)
    G.add_nodes_from(R_nodes_15)
    G.add_edges_from(R_edges_15)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_15 + [n for u, v, _ in L_edges_15 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_15 + [n for u, v, _ in R_edges_15 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())


    ###########################################################################################################
    # 创建图16
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_swing_limb_joint")

    # 添加左子图及其节点和边
    L_nodes_16 = []
    L_edges_16 = [("parent", "child", {"require_label":"limb_joint"})]

    # 添加右子图及其节点和边
    R_nodes_16 = []
    R_edges_16 = [("parent", "child", {"type":"hinge", "joint_axis":"0 1 0"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_16)
    G.add_edges_from(L_edges_16)
    G.add_nodes_from(R_nodes_16)
    G.add_edges_from(R_edges_16)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_16 + [n for u, v, _ in L_edges_16 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_16 + [n for u, v, _ in R_edges_16 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())    


    ###########################################################################################################
    # 创建图17
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_acute_lift_limb_joint")

    # 添加左子图及其节点和边
    L_nodes_17 = []
    L_edges_17 = [("parent", "child", {"require_label":"limb_joint"})]

    # 添加右子图及其节点和边
    R_nodes_17 = []
    R_edges_17 = [("parent", "child", {"type":"hinge","axis_angle":"0 0 1 120", "joint_axis":"0 0 1"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_17)
    G.add_edges_from(L_edges_17)
    G.add_nodes_from(R_nodes_17)
    G.add_edges_from(R_edges_17)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_17 + [n for u, v, _ in L_edges_17 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_17 + [n for u, v, _ in R_edges_17 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())    



    ###########################################################################################################
    # 创建图18
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_obtuse_lift_limb_joint")

    # 添加左子图及其节点和边
    L_nodes_18 = []
    L_edges_18 = [("parent", "child", {"require_label":"limb_joint"})]

    # 添加右子图及其节点和边
    R_nodes_18 = []
    R_edges_18 = [("parent", "child", {"type":"hinge","axis_angle":"0 0 1 60", "joint_axis":"0 0 1"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_18)
    G.add_edges_from(L_edges_18)
    G.add_nodes_from(R_nodes_18)
    G.add_edges_from(R_edges_18)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_18 + [n for u, v, _ in L_edges_18 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_18 + [n for u, v, _ in R_edges_18 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())   


    ###########################################################################################################
    # 创建图19
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_backwards_lift_limb_joint")

    # 添加左子图及其节点和边
    L_nodes_19 = []
    L_edges_19 = [("parent", "child", {"require_label":"limb_joint"})]

    # 添加右子图及其节点和边
    R_nodes_19 = []
    R_edges_19 = [("parent", "child", {"type":"hinge","axis_angle":"0 0 1 -60", "joint_axis":"0 0 1"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes_19)
    G.add_edges_from(L_edges_19)
    G.add_nodes_from(R_nodes_19)
    G.add_edges_from(R_edges_19)
    G.add_node("testnode",info = {"sub":"L","infom":"666"})
    # 创建左子图
    L_subgraph = G.subgraph(L_nodes_19 + [n for u, v, _ in L_edges_19 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes_19 + [n for u, v, _ in R_edges_19 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())  



    for idx, graph in enumerate(graphs):
        # print(f"\nGraph {idx} - {graph.name}")
        
        # # # 打印节点信息
        # # print("Nodes:")
        # # for node in graph.nodes(data=True):
        # #     print(f"  Node: {node}")

        # # # 打印边信息
        # # print("Edges:")
        # # for edge in graph.edges(data=True):
        # #     print(f"  Edge: {edge}")

        # # 打印左子图信息
        # left_subgraph_nodes = graph.subgraph(locals()[f"L_nodes_{idx}"] + [n for u, v, _ in locals()[f"L_edges_{idx}"] for n in [u, v]])
        # print("Left Subgraph Nodes:")
        # for node in left_subgraph_nodes.nodes(data=True):
        #     print(f"  Node: {node}")

        # print("Left Subgraph Edges:")
        # for edge in left_subgraph_nodes.edges(data=True):
        #     print(f"  Edge: {edge}")

        # # 打印右子图信息
        # right_subgraph_nodes = graph.subgraph(locals()[f"R_nodes_{idx}"] + [n for u, v, _ in locals()[f"R_edges_{idx}"] for n in [u, v]])
        # print("Right Subgraph Nodes:")
        # for node in right_subgraph_nodes.nodes(data=True):
        #     print(f"  Node: {node}")

        # print("Right Subgraph Edges:")
        # for edge in right_subgraph_nodes.edges(data=True):
        #     print(f"  Edge: {edge}")


        # 存储左右子图信息到字典
        subgraph_info[idx] = {
            'left_nodes': locals()[f"L_nodes_{idx}"],
            'left_edges': locals()[f"L_edges_{idx}"],
            'right_nodes': locals()[f"R_nodes_{idx}"],
            'right_edges': locals()[f"R_edges_{idx}"],
        }

    return graphs, subgraph_info







def read_graph_info(num):
    # 示例调用
    all_graphs, subgraph_info_dict = my_graph()
    # print("--------------------test-------------------------")
    # print("-------------warning:counting from 0-------------")
    # print(f"Graph {num}")
    # 访问图的左右子图信息示例
    '''
    from 0 to the last graph
    '''
    # print(all_graphs[num].name)
    left_nodes = subgraph_info_dict[num]['left_nodes']
    # print("left_nodes",left_nodes)

    left_edges = subgraph_info_dict[num]['left_edges']
    # print("left_edges",left_edges)

    right_nodes = subgraph_info_dict[num]['right_nodes']
    # print("right_nodes",right_nodes)

    right_edges = subgraph_info_dict[num]['right_edges']
    # print("right_edges",right_edges)


read_graph_info(19)