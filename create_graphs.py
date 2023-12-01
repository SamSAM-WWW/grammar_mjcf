import networkx as nx
graphs = []
'''
发现确实从dot文件读取难度巨大 通过直接在python代码中构建就简单很多
'''

# 创建图1
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
L_subgraph = G.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]])

# 创建右子图
R_subgraph = G.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]])

# store in graphs
graphs.append(G.copy())


G.clear()



# 创建图2
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
L_subgraph = G.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]])

# 创建右子图
R_subgraph = G.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]])

# store in graphs
graphs.append(G.copy())



































































# 输出graphs[0]的左子图和右子图
first_graph = graphs[0]
L_subgraph_first = first_graph.subgraph(L_nodes + [n for u, v, _ in L_edges for n in [u, v]])
R_subgraph_first = first_graph.subgraph(R_nodes + [n for u, v, _ in R_edges for n in [u, v]])

# 访问graphs[0]的左子图节点和边
print("Left Subgraph Nodes:", [(n) for n in L_subgraph_first.nodes])
print("Left Subgraph Edges:", [(u, v, L_subgraph_first[u][v]) for u, v in L_subgraph_first.edges])

# 访问graphs[0]的右子图节点和边
print("Right Subgraph Nodes:", [(n) for n in R_subgraph_first.nodes])
print("Right Subgraph Edges:", [(u, v, R_subgraph_first[u][v]) for u, v in R_subgraph_first.edges])