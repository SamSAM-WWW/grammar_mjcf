import numpy as np
from scipy.spatial.transform import Rotation 
from RobotGraph import RobotJoint,RobotLink,RobotGraph
import quaternion

def euler2quaternion(euler):
    '''
    欧拉角转四元数
    '''
    # r = Rotation.from_euler('xyz', euler, degrees=True)
    r = Rotation.from_euler('xyz', euler, degrees=True)
    quaternion = r.as_quat()
    np_quaternion = np.quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3])
    return np_quaternion

def quaternion_coords(q):
    """Get the coefficients of a Quaternion as an np.ndarray."""
    return np.array([q.w, q.x, q.y, q.z])

def one_hot_encode(enum_member):
    """Encode an enum member as a one-hot vectorobot_graph."""
    vec = np.zeros(len(type(enum_member).__members__))
    vec[int(enum_member)] = 1
    return vec

def featurize_link(link):
    """Extract a feature vector from a rd.Link."""
    return np.array([*one_hot_encode(link.joint_type),
                    link.joint_pos,
                    *euler2quaternion(link.joint_rot),
                    *link.joint_axis,
                    *one_hot_encode(link.shape),
                    link.length,
                    link.radius,
                    link.density,
                    link.friction,
                    link.joint_kp,
                    link.joint_kd,
                    link.joint_torque,
                    *one_hot_encode(link.joint_control_mode)])

class Preprocessor:
    def __init__(self, all_labels = None,max_nodes=None):
        self.max_nodes = max_nodes
        self.all_labels = all_labels
    
    '''
    预处理图数据，将其转换为适用于 GNN 的数据格式
    ---------------
    输入:
        - robot_graph: 自定义的机器人图数据结构
        - all_labels
        - max_nodes: 节点的最大数量（可选）

    输出:
        - 邻接矩阵
        - 节点特征
        - 掩码
    '''
    def get_pos_rot(self, robot_graph):
        pos_rot = []

        # 遍历机器人图中的每个连杆节点
        for node_name, node_data in robot_graph.nodes(data=True):
            # 检查节点是否是连杆节点
            if node_data['type'] == 'link':
                # 获取当前连杆节点的信息
                link_info = node_data['info']
                
                # 获取当前连杆节点的父节点名称
                parent_nodes = list(robot_graph.predecessors(node_name))
                
                # 初始化父节点的位置和旋转信息
                if parent_nodes:
                    parent_node_name = parent_nodes[0]  # 假设每个连杆只有一个父节点
                    parent_pos, parent_rot = pos_rot[parent_node_name]
                    parent_link_length = robot_graph.nodes[parent_node_name]['info'].length
                else:
                    parent_pos, parent_rot = np.zeros(3), np.quaternion(1, 0, 0, 0)
                    parent_link_length = 0

                # 计算当前连杆节点的世界位置
                offset = np.array([parent_link_length * link_info.body_pos[0], 0, 0])
                rel_pos = quaternion.rotate_vectors(parent_rot, offset)
                pos = parent_pos + rel_pos

                # 计算当前连杆节点的世界旋转
                rel_rot = quaternion(link_info.euler).conjugate()
                rot = parent_rot * rel_rot
                
                # 将当前连杆节点的世界位置和旋转信息添加到 pos_rot 列表中
                pos_rot.append((pos, rot))
        return pos_rot
    def preprocess(self, robot_graph, max_nodes=None):
        

        # 现在 pos_rot 列表中存储了所有连杆节点的世界位置和旋转信息
        # 在这里使用父节点的信息来计算当前link的世界位置和旋转
        # 获取图中的节点和边信息
        nodes = robot_graph.nodes
        edges = robot_graph.edges

        # 构建邻接矩阵
        adj_matrix = self.build_adjacency_matrix(nodes, edges)

        # 提取节点特征
        node_features = self.extract_node_features(nodes)
        masks = None
        # 创建掩码
        if max_nodes is not None:
            masks = self.create_masks(nodes, max_nodes)

        return adj_matrix, node_features, masks

    def build_adjacency_matrix(self, robot_graph):
        #判断graph里 link的数量
        num_nodes = 0
        for n in robot_graph.successors('root'):
            if robot_graph.nodes[n]['type'] == 'link':
                num_nodes = num_nodes + 1

        adj_matrix = np.zeros((num_nodes, num_nodes))

        # 遍历关节节点，构建邻接矩阵
        joint_nodes = [node for node in robot_graph.nodes if robot_graph.nodes[node]['type'] == 'joint']
        for node in joint_nodes:
            children = list(robot_graph.successors(node))[0] if list(robot_graph.successors(node)) else None
            parent = list(robot_graph.predecessors(node))[0] if list(robot_graph.predecessors(node)) else None
            parent_index = joint_nodes.index(parent)
            child_index = joint_nodes.index(children)
            adj_matrix[parent_index, child_index] = 1
            adj_matrix[child_index, parent_index] = 1
        return adj_matrix

    def extract_node_features(self, robot_graph,pos_rot):
        # 在这里实现提取节点特征的逻辑
        # 请根据您的图结构自行设计节点特征的提取方法
        # 返回节点特征的 numpy 数组.

        link_features = []
        links = [node_info for _, node_info in robot_graph.nodes(data='info') if isinstance(node_info, RobotLink)]
        for i, link in enumerate(links):
            world_pos, world_rot = pos_rot[i]
            world_joint_axis = quaternion.rotate_vectors(world_rot, link.joint_axis)
            label_vec = np.zeros(len(self.all_labels))
            label_vec[self.all_labels.index(link.label)] = 1
        
        link_features.append(np.array([
                *featurize_link(link),
                *world_pos,
                *quaternion_coords(world_rot),
                *world_joint_axis,
                *label_vec]))
        
        link_features = np.array(link_features)

        return link_features
        

    def create_masks(self, nodes, max_nodes):
        num_nodes = len(nodes)
        if max_nodes is None:
            max_nodes = self.max_nodes
        masks = np.zeros(num_nodes, dtype=bool)
        masks[:num_nodes] = True
        return masks