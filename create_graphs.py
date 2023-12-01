import networkx as nx
graphs = []

def my_graph():
    
    '''
    发现确实从dot文件读取难度巨大 通过直接在python代码中构建就简单很多

    return a list of all the graphs
    ----------
    '''
    ###########################################################################################################
    # 创建图1 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_robot")

    # 添加左子图及其节点和边
    L_nodes = ["robot"]
    L_edges = []

    # 添加右子图及其节点和边
    R_nodes = ["head", "body", "tail"]
    R_edges = [("head", "body", {"label": "body_joint"}), ("body", "tail", {"label": "body_joint"})]

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

    # store in graphs
    graphs.append(G.copy())


    G.clear()


    ###########################################################################################################
    # 创建图2 边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="append_body")

    # 添加左子图及其节点和边
    L_nodes = ["tail"]
    L_edges = [("parent","tail",{"id": "parent_edges"})]

    # 添加右子图及其节点和边
    R_nodes = ["tail", "body"]
    R_edges = [("parent", "body", {"id": "parent_edges"}), ("body", "tail", {"label": "body_joint"})]

    # 向根图添加左右两个子图
    G.add_nodes_from(L_nodes)
    G.add_nodes_from(R_nodes)
    G.add_edges_from(R_edges)

    # 创建左子图
    L_subgraph = G.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # 创建右子图
    R_subgraph = G.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()
    # 添加右子图专属属性...

    # store in graphs
    graphs.append(G.copy())

    ###########################################################################################################
    # 创建图3  边的属性必须写，如果是空必须写成{}，否则读取bug
    G = nx.DiGraph(name="make_body_with_legs")

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





























































    # 输出graphs[0]的左子图和右子图
    first_graph = graphs[4]
    L_subgraph_first = first_graph.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]]).copy()
    R_subgraph_first = first_graph.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]]).copy()

    # 访问graphs[0]的左子图节点和边
    print("Left Subgraph Nodes:", [(n) for n in L_subgraph_first.nodes])
    print("Left Subgraph Edges:", [(u, v, L_subgraph_first[u][v]) for u, v in L_subgraph_first.edges])

    # 访问graphs[0]的右子图节点和边
    print("Right Subgraph Nodes:", [(n) for n in R_subgraph_first.nodes])
    print("Right Subgraph Edges:", [(u, v, R_subgraph_first[u][v]) for u, v in R_subgraph_first.edges])

    # body_attributes = R_subgraph.nodes["body"]
    # print("Rsub_body_attr",body_attributes)
    # body_attributes = L_subgraph.nodes["body"]
    # print("Lsub_body_attr",body_attributes)
    
    return graphs