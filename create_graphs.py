import networkx as nx


def my_graph():
    graphs = []
    '''
    发现确实从dot文件读取难度巨大 通过直接在python代码中构建就简单很多

    return a list of all the graphs
    ----------
    '''
    ###########################################################################################################
    # 创建图0 边的属性必须写，如果是空必须写成{}，否则读取bug
    G0 = nx.DiGraph(name="make_robot")

    # 添加左子图及其节点和边
    L_nodes_0 = ["robot"]
    L_edges_0 = []

    # 添加右子图及其节点和边
    R_nodes_0 = ["head", "body", "tail"]
    R_edges_0 = [("head", "body", {"label": "body_joint"}), ("body", "tail", {"label": "body_joint"})]

    # 向根图添加左右两个子图
    G0.add_nodes_from(L_nodes_0)
    G0.add_nodes_from(R_nodes_0)
    G0.add_edges_from(R_edges_0)

    # 创建左子图
    L_subgraph = G0.subgraph(L_nodes_0 + [n for u, v, _ in L_edges_0 for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G0.subgraph(R_nodes_0 + [n for u, v, _ in R_edges_0 for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G0)




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
    R_nodes_3 = ["body"]
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




















    for idx, graph in enumerate(graphs):
        print(f"\nGraph {idx} - {graph.name}")
        
        # 打印节点信息
        print("Nodes:")
        for node in graph.nodes(data=True):
            print(f"  Node: {node}")

        # 打印边信息
        print("Edges:")
        for edge in graph.edges(data=True):
            print(f"  Edge: {edge}")

        # 打印左子图信息
        left_subgraph_nodes = graph.subgraph(locals()[f"L_nodes_{idx}"] + [n for u, v, _ in locals()[f"L_edges_{idx}"] for n in [u, v]])
        print("Left Subgraph Nodes:")
        for node in left_subgraph_nodes.nodes(data=True):
            print(f"  Node: {node}")

        print("Left Subgraph Edges:")
        for edge in left_subgraph_nodes.edges(data=True):
            print(f"  Edge: {edge}")

        # 打印右子图信息
        right_subgraph_nodes = graph.subgraph(locals()[f"R_nodes_{idx}"] + [n for u, v, _ in locals()[f"R_edges_{idx}"] for n in [u, v]])
        print("Right Subgraph Nodes:")
        for node in right_subgraph_nodes.nodes(data=True):
            print(f"  Node: {node}")

        print("Right Subgraph Edges:")
        for edge in right_subgraph_nodes.edges(data=True):
            print(f"  Edge: {edge}")

    return graphs



my_graph()