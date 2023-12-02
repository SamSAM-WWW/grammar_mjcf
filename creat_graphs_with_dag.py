from DAG import DAG
graphs = []
class TwoSubgraphDAG(DAG):
    def __init__(self, name=None):
        super().__init__(name)
        self.lr_subgraph = {'L': DAG(), 'R': DAG()}

    def add_node_to_subgraph(self, node_name, subgraph_key, info=None):
        """ Add a node to the specified LR subgraph. """
        if subgraph_key not in self.lr_subgraph:
            raise ValueError(f"Invalid subgraph key: {subgraph_key}")
        self.lr_subgraph[subgraph_key].add_node(node_name, info=info)

    def add_edge_to_subgraph(self, ind_node, dep_node, subgraph_key, info=None):
        """ Add an edge to the specified LR subgraph. """
        if subgraph_key not in self.lr_subgraph:
            raise ValueError(f"Invalid subgraph key: {subgraph_key}")
        self.lr_subgraph[subgraph_key].add_edge(ind_node, dep_node, info=info)

    # You can add more methods as needed for handling LR subgraphs
    # ...


# 创建 TwoSubgraphDAG 实例
lr_dag = TwoSubgraphDAG(name="make_robot")

# 向 L 子图添加节点
lr_dag.add_node_to_subgraph("robot", "L", info={"require_label": "robot"})

# 向 R 子图添加节点和边
lr_dag.add_node_to_subgraph("head", "R", info={"label": "head"})
lr_dag.add_node_to_subgraph("body", "R", info={"label": "body"})
lr_dag.add_node_to_subgraph("tail", "R", info={"label": "tail"})
lr_dag.add_edge_to_subgraph("head", "body", "R", info={"label": "body_joint"})
lr_dag.add_edge_to_subgraph("body", "tail", "R", info={"label": "body_joint"})


# print(lr_dag.lr_subgraph['L'].node_info)
# print(lr_dag.lr_subgraph['L'].edge_info)  # 打印边信息
# print(lr_dag.lr_subgraph['R'].node_info)
# print(lr_dag.lr_subgraph['R'].edge_info)  # 打印边信息

graphs.append(lr_dag)
print(graphs[0].lr_subgraph['L'].node_info)