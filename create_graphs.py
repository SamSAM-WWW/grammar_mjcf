import networkx as nx


def my_graph():
    graphs = []
    '''
    发现确实从dot文件读取难度巨大 通过直接在python代码中构建就简单很多

    return a list of all the graphs
    ----------
    '''
    ###########################################################################################################
    # 创建图1 边的属性必须写，如果是空必须写成{}，否则读取bug
    G1 = nx.DiGraph(name="makea_robot")

    # 添加左子图及其节点和边
    L_nodes = ["robot"]
    L_edges = []

    # 添加右子图及其节点和边
    R_nodes = ["head", "body", "tail"]
    R_edges = [("head", "body", {"label": "body_joint"}), ("body", "tail", {"label": "body_joint"})]

    # 向根图添加左右两个子图
    G1.add_nodes_from(L_nodes)
    G1.add_nodes_from(R_nodes)
    G1.add_edges_from(R_edges)

    # 创建左子图
    L_subgraph = G1.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G1.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G1.copy())




    ###########################################################################################################
    # 创建图2 边的属性必须写，如果是空必须写成{}，否则读取bug
    G2 = nx.DiGraph(name="append_body")

    # 添加左子图及其节点和边
    L_nodes = ["tail"]
    L_edges = [("parent","tail",{"id": "parent_edges"})]

    # 添加右子图及其节点和边
    R_nodes = ["tail", "body"]
    R_edges = [("parent", "body", {"id": "parent_edges"}), ("body", "tail", {"label": "body_joint"})]

    # 向根图添加左右两个子图
    G2.add_nodes_from(L_nodes)
    G2.add_nodes_from(R_nodes)
    G2.add_edges_from(R_edges)

    # 创建左子图
    L_subgraph = G2.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # 创建右子图
    R_subgraph = G2.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G2.copy())


    ###########################################################################################################
    # 创建图3  边的属性必须写，如果是空必须写成{}，否则读取bug
    G3 = nx.DiGraph(name="make_body_with_legs")

    # 添加左子图及其节点和边
    L_nodes = ["body"]
    L_edges = []

    # 添加右子图及其节点和边
    R_nodes = ["body", "limb_mount", "limb_link", "limb"]
    R_edges = [("body", "limb_mount", {"type": "fixed", "offset":0.5, "axis_angle":"0 1 0 90"}),
                ("body", "limb_mount", {"type": "fixed", "offset":0.5, "axis_angle":"0 1 0 90", "mirror":True}), 
                ("limb_mount", "limb_link", {"label": "limb_joint"}), 
                ("limb_link","limb",{})]

    # 向根图添加左右两个子图
    G3.add_nodes_from(L_nodes)
    G3.add_nodes_from(R_nodes)
    G3.add_edges_from(R_edges)
    # 创建左子图
    L_subgraph = G3.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G3.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...
    R_subgraph.nodes["body"].update(shape="capsule", length=0.15, radius=0.045, density=3.0)

    # store in graphs
    graphs.append(G3.copy())


    ###########################################################################################################
    # 创建图4
    G = nx.DiGraph(name="make_body_without_legs")

    # 添加左子图及其节点和边
    L_nodes = ["body"]
    L_edges = []

    # 添加右子图及其节点和边
    R_nodes = ["body"]
    R_edges = []

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes)
    G.add_nodes_from(R_nodes)
    G.add_edges_from(R_edges)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...
    R_subgraph.nodes["body"].update(shape="capsule", length=0.15, radius=0.045, density=3.0)

    # store in graphs
    graphs.append(G.copy())



    ###########################################################################################################
    # 创建图5
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="append_limb_link")

    # 添加左子图及其节点和边
    L_nodes = ["limb"]
    L_edges = [("parent","limb",{})]

    # 添加右子图及其节点和边
    R_nodes = ["limb","limb_link"]
    R_edges = [("parent","limb_link",{"label":"limb_joint"}),("limb_link","limb",{})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes)
    G.add_edges_from(L_edges)
    G.add_nodes_from(R_nodes)
    G.add_edges_from(R_edges)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...


    # store in graphs
    graphs.append(G.copy())


    ###########################################################################################################
    # 创建图6
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="end_limb")

    # 添加左子图及其节点和边
    L_nodes = ["limb"]
    L_edges = [("parent","limb",{})]

    # 添加右子图及其节点和边
    R_nodes = ["parent"]
    R_edges = []

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes)
    G.add_edges_from(L_edges)
    G.add_nodes_from(R_nodes)
    G.add_edges_from(R_edges)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...


    # store in graphs
    graphs.append(G.copy())



    ###########################################################################################################
    # 创建图7
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="end_tail")

    # 添加左子图及其节点和边
    L_nodes = ["tail"]
    L_edges = [("parent","tail",{})]

    # 添加右子图及其节点和边
    R_nodes = ["parent"]
    R_edges = []

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes)
    G.add_edges_from(L_edges)
    G.add_nodes_from(R_nodes)
    G.add_edges_from(R_edges)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...


    # store in graphs
    graphs.append(G.copy())




    ###########################################################################################################
    # 创建图8
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="end_head").copy()

    # 添加左子图及其节点和边
    L_nodes = ["head"]
    L_edges = [("head","child",{})]

    # 添加右子图及其节点和边
    R_nodes = ["child"]
    R_edges = []

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes)
    G.add_edges_from(L_edges)
    G.add_nodes_from(R_nodes)
    G.add_edges_from(R_edges)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...


    # store in graphs
    graphs.append(G.copy())





    ###########################################################################################################
    # 创建图9
    # 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_normal_limb_link")

    # 添加左子图及其节点和边
    L_nodes = ["limb_link"]
    L_edges = []

    # 添加右子图及其节点和边
    R_nodes = ["limb_link"]
    R_edges = []

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes)
    G.add_edges_from(L_edges)
    G.add_nodes_from(R_nodes)
    G.add_edges_from(R_edges)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    # 添加左子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...
    R_subgraph.nodes["limb_link"].update(shape="capsule", length=0.15, radius=0.025)

    # store in graphs
    graphs.append(G.copy())





























    #输出所有的graph信息
    for idx, graph in enumerate(graphs):
        print(f"\nGraph {idx} - {graph.name}")
        for node in graph.nodes(data=True):
            print(f"Node: {node}")
        for edge in graph.edges(data=True):
            print(f"Edge: {edge}")

    selected_graph = graphs[1]


    # # 打印选定图的信息
    # print(f"\nSelected Graph - {selected_graph.name}")
    # for node in selected_graph.nodes(data=True):
    #     print(f"Node: {node}")
    # for edge in selected_graph.edges(data=True):
    #     print(f"Edge: {edge}")



    
    return graphs



my_graph()