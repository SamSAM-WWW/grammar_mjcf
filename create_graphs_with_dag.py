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




def create_graphs_1():
    # 创建 TwoSubgraphDAG 实例0
    lr_dag = TwoSubgraphDAG(name="make_robot")

    # 向 L 子图添加节点和边
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
    # print(graphs[0].lr_subgraph['L'].node_info)



    #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例1
    lr_dag = TwoSubgraphDAG(name="append_body")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("tail", "L", info={"require_label": "tail"})
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_edge_to_subgraph("parent","tail","L",info={"id":"parent_edges"})
    # 向 R 子图添加节点和边
    lr_dag.add_node_to_subgraph("tail", "R", info={"label": "tail"})
    lr_dag.add_node_to_subgraph("body", "R", info={"label": "body"})
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_edge_to_subgraph("parent","body","R",info={"id":"parent_edges"})
    lr_dag.add_edge_to_subgraph("body", "tail", "R", info={"label": "body_joint"})
    graphs.append(lr_dag)



    #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例2
    lr_dag = TwoSubgraphDAG(name="make_body_with_legs")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("body", "L", info={"require_label": "body"})

    # 向 R 子图添加节点和边
    lr_dag.add_node_to_subgraph("body", "R", info={"label": "body"})
    lr_dag.add_node_to_subgraph("limb_mount", "R", info={"shape": "capsule", "length":0.15, "radius":0.025})
    lr_dag.add_node_to_subgraph("limb_link", "R", info={"label": "limb_link"})
    lr_dag.add_node_to_subgraph("limb", "R", info={"label": "limb"})

    lr_dag.add_edge_to_subgraph("body","limb_mount","R",info={"type":"fixed", "offset":0.5, "axis_angle":"0 1 0 90"})
    lr_dag.add_edge_to_subgraph("body","limb_mount","R",info={"type":"fixed", "offset":0.5, "axis_angle":"0 1 0 90", "mirror":True})
    lr_dag.add_edge_to_subgraph("limb_mount","limb_link","R",info={"label":"limb_joint"})
    lr_dag.add_edge_to_subgraph("limb_link","limb","R",info={"defalt":"defalt_edge"})
    graphs.append(lr_dag)

    #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例3
    lr_dag = TwoSubgraphDAG(name="make_body_without_legs")

    # 向 L 子图添加节点
    lr_dag.add_node_to_subgraph("body", "L", info={"require_label": "body"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("body", "R", info={"shape": "capsule", "length": 0.15, "radius": 0.045, "density": 3.0})
    graphs.append(lr_dag)

    #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例4
    lr_dag = TwoSubgraphDAG(name="append_limb_link")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("limb", "L", info={"require_label": "limb"})
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_edge_to_subgraph("parent", "limb", "L", info={"defalt":"defalt_edge"})

    # 向 R 子图添加节点和边
    lr_dag.add_node_to_subgraph("limb", "R", info={"label": "limb"})
    lr_dag.add_node_to_subgraph("limb_link", "R", info={"label": "limb_link"})
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_edge_to_subgraph("parent", "limb_link", "R", info={"label": "limb_joint"})
    lr_dag.add_edge_to_subgraph("limb_link", "limb", "R", info={"defalt":"defalt_edge"})
    graphs.append(lr_dag)


    #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例5
    lr_dag = TwoSubgraphDAG(name="end_limb")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("limb", "L", info={"require_label": "limb"})
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_edge_to_subgraph("parent", "limb", "L", info={"defalt":"defalt_edge"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    graphs.append(lr_dag)


    #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例6
    lr_dag = TwoSubgraphDAG(name="end_tail")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("tail", "L", info={"require_label": "tail"})
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_edge_to_subgraph("parent", "tail", "L", info={"defalt":"defalt_edge"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    graphs.append(lr_dag)


    #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例7
    lr_dag = TwoSubgraphDAG(name="end_head")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("head", "L", info={"require_label": "head"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("head", "child", "L", info={"defalt":"defalt_edge"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    graphs.append(lr_dag)


    #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例8
    lr_dag = TwoSubgraphDAG(name="make_normal_limb_link")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("limb_link", "L", info={"require_label": "limb_link"})


    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("limb_link", "R", info={"shape": "capsule","length": 0.1,"radius": 0.025})
    graphs.append(lr_dag)


        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例9
    lr_dag = TwoSubgraphDAG(name="make_long_limb_link")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("limb_link", "L", info={"require_label": "limb_link"})


    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("limb_link", "R", info={"shape": "capsule","length": 0.15,"radius": 0.025})
    graphs.append(lr_dag)



        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例10
    lr_dag = TwoSubgraphDAG(name="make_fixed_body_joint")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "L", info={"require_label": "body_joint"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "R", info={"type": "fixed"})
    graphs.append(lr_dag)    



        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例11
    lr_dag = TwoSubgraphDAG(name="make_roll_body_joint")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "L", info={"require_label": "body_joint"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "R", info={"type": "hinge","joint_axis":"1 0 0"})
    graphs.append(lr_dag)    



        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例12
    lr_dag = TwoSubgraphDAG(name="make_swing_body_joint")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "L", info={"require_label": "body_joint"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "R", info={"type": "hinge","joint_axis":"0 1 0"})
    graphs.append(lr_dag)    



        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例13
    lr_dag = TwoSubgraphDAG(name="make_lift_body_joint")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "L", info={"require_label": "body_joint"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "R", info={"type": "hinge","joint_axis":"0 0 1"})
    graphs.append(lr_dag)    


        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例14
    lr_dag = TwoSubgraphDAG(name="make_left_roll_limb_joint")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "L", info={"require_label": "limb_joint"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "R", info={"type": "hinge","axis_angle":"0 1 0 -90","joint_axis":"1 0 0"})
    graphs.append(lr_dag)    




        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例15
    lr_dag = TwoSubgraphDAG(name="make_right_roll_limb_joint")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "L", info={"require_label": "limb_joint"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "R", info={"type": "hinge","axis_angle":"0 1 0 90","joint_axis":"1 0 0"})
    graphs.append(lr_dag)


        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例16
    lr_dag = TwoSubgraphDAG(name="make_swing_limb_joint")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "L", info={"require_label": "limb_joint"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "R", info={"type": "hinge","joint_axis":"0 1 0"})
    graphs.append(lr_dag)

        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例17
    lr_dag = TwoSubgraphDAG(name="make_acute_lift_limb_joint")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "L", info={"require_label": "limb_joint"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "R", info={"type": "hinge","axis_angle":"0 0 1 120","joint_axis":"0 0 1"})
    graphs.append(lr_dag)



        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例18
    lr_dag = TwoSubgraphDAG(name="make_obtuse_lift_limb_joint")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "L", info={"require_label": "limb_joint"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "R", info={"type": "hinge","axis_angle":"0 0 1 60","joint_axis":"0 0 1"})
    graphs.append(lr_dag)

        #-------------------------------------------------------
    # 创建 TwoSubgraphDAG 实例19
    lr_dag = TwoSubgraphDAG(name="make_backwards_lift_limb_joint")

    # 向 L 子图添加节点和边
    lr_dag.add_node_to_subgraph("parent", "L", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "L", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "L", info={"require_label": "limb_joint"})

    # 向 R 子图添加节点
    lr_dag.add_node_to_subgraph("parent", "R", info={"require_label": "parent"})
    lr_dag.add_node_to_subgraph("child", "R", info={"require_label": "child"})
    lr_dag.add_edge_to_subgraph("parent", "child", "R", info={"type": "hinge","axis_angle":"0 0 1 -60","joint_axis":"0 0 1"})
    graphs.append(lr_dag)






    return graphs


def create_graphs(graph_num):
    '''
    choose which graph U want to use
    -----
    input a number, range: from 1 to the end
    '''
    if graph_num == 1:
        return create_graphs_1()

    if graph_num == 2:
        pass





































# i = 0
# graphs = create_graphs(1)
# print(graphs[i].lr_subgraph['L'].node_info)
# print(graphs[i].lr_subgraph['L'].edge_info)
# print(graphs[i].lr_subgraph['R'].node_info)
# print(graphs[i].lr_subgraph['R'].edge_info)