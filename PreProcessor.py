import numpy as np
from scipy.spatial.transform import Rotation 
from RobotGraph import RobotJoint,RobotLink,RobotGraph
import quaternion
from enum import Enum

class LinkType(Enum):
    capsule = 0
    cylinder = 1
    box = 2
    sphere = 3
    ellipsoid = 4 


def euler2quaternion(euler):
    '''
    欧拉角转四元数
    '''
    # Convert Euler angles to quaternion
    q = np.quaternion(*euler, degrees=True)
    return q

def quaternion_coords(q):
    """Get the coefficients of a Quaternion as an np.ndarray."""
    return np.array([q.w, q.x, q.y, q.z])

def one_hot_encode(enum_member):
    """Encode an enum member as a one-hot vector."""
    vec = np.zeros(len(LinkType))  # 使用枚举类的长度来初始化向量
    vec[enum_member.value] = 1  # 将枚举成员的值对应的索引位置设为1
    return vec

def featurize_link(link):
    """Extract a feature vector from a rd.Link."""
    link_type_enum = LinkType[link.link_type]
    if link.link_type != 'box':
        return np.array([*one_hot_encode(link_type_enum),
                        link.size,
                        *link.start_point,
                        *link.geom_pos,
                        *link.body_pos,
                        link.density,
                        *link.euler,
                        link.density,
                        ])
    else:
        size_x, size_y, size_z = map(float, link.size.split())  # 假设尺寸参数以空格分隔
        size_all = (size_x+size_y+size_z)*0.33
        return np.array([*one_hot_encode(link_type_enum),
                        size_all,
                        *link.start_point,
                        *link.geom_pos,
                        *link.body_pos,
                        link.density,
                        *link.euler,
                        link.density,
                        ])

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
    # def get_pos_rot(self, robot_graph):
    #     pos_rot = []

    #     # 遍历机器人图中的每个连杆节点
    #     for node_name, node_data in robot_graph.nodes(data=True):
    #         # 检查节点是否是连杆节点
    #         if node_data['type'] == 'link':
    #             # 获取当前连杆节点的信息
    #             link_info = node_data['info']
                
    #             # 获取当前连杆节点的父节点名称
    #             parent_nodes = list(robot_graph.predecessors(node_name))
                
    #             # 初始化父节点的位置和旋转信息
    #             if parent_nodes:
    #                 parent_node_name = parent_nodes[0]  # 假设每个连杆只有一个父节点
    #                 parent_pos, parent_rot = pos_rot[parent_node_name]
    #                 parent_link_length = robot_graph.nodes[parent_node_name]['info'].length
    #             else:
    #                 parent_pos, parent_rot = np.zeros(3), np.quaternion(1, 0, 0, 0)
    #                 parent_link_length = 0

    #             # 计算当前连杆节点的世界位置
    #             offset = np.array([parent_link_length * link_info.body_pos[0], 0, 0])
    #             rel_pos = quaternion.rotate_vectors(parent_rot, offset)
    #             pos = parent_pos + rel_pos

    #             # 计算当前连杆节点的世界旋转
    #             # print("link_info.euler",link_info.euler)
    #             # print("quaternion(link_info.euler)",quaternion.from_euler_angles(link_info.euler))
    #             rel_rot = quaternion.from_euler_angles(link_info.euler).conjugate()
    #             rot = parent_rot * rel_rot
                
    #             # 将当前连杆节点的世界位置和旋转信息添加到 pos_rot 列表中
    #             pos_rot.append((pos, rot))
    #     return pos_rot
    def get_pos_rot(self, robot_graph):
        pos_rot = {}

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
                    parent_pos, parent_rot = pos_rot.get(parent_node_name, (np.zeros(3), np.quaternion(1, 0, 0, 0)))
                else:
                    parent_pos, parent_rot = np.zeros(3), np.quaternion(1, 0, 0, 0)
                    

                # 计算当前连杆节点的世界位置
                offset = np.array([1 * link_info.body_pos[0], 0, 0])
                rel_pos = quaternion.rotate_vectors(parent_rot, offset)
                pos = parent_pos + rel_pos

                # 计算当前连杆节点的世界旋转
                rel_rot = quaternion.from_euler_angles(link_info.euler).conjugate()
                rot = parent_rot * rel_rot
                
                # 将当前连杆节点的世界位置和旋转信息添加到 pos_rot 字典中
                pos_rot[node_name] = (pos, rot)
        return pos_rot
    def preprocess(self, robot_graph, max_nodes = None):
        

        # 现在 pos_rot 列表中存储了所有连杆节点的世界位置和旋转信息
        # 在这里使用父节点的信息来计算当前link的世界位置和旋转
        # 获取图中的节点和边信息
        nodes = robot_graph.nodes
        edges = robot_graph.edges

        # 构建邻接矩阵
        adj_matrix = self.build_adjacency_matrix(robot_graph)
        pos_rot = self.get_pos_rot(robot_graph)
        # 提取节点特征
        node_features = self.extract_node_features(robot_graph,pos_rot)
        masks = None
        # 创建掩码
        if max_nodes is None:
            max_nodes = self.max_nodes

        if max_nodes is not None:
            if max_nodes > len(node_features):
                adj_matrix, node_features, masks = self.pad_graph(adj_matrix, node_features, max_nodes)
            else:
                masks = np.full(len(node_features), True)
        return adj_matrix, node_features, masks

    def build_adjacency_matrix(self, robot_graph):
        # 判断graph里 link的数量
        

        

        # 遍历关节节点，构建邻接矩阵
        link_nodes = [node for node in robot_graph.nodes if robot_graph.nodes[node]['type'] == 'link']
        joint_nodes = [node for node in robot_graph.nodes if robot_graph.nodes[node]['type'] == 'joint']
        num_nodes = len(link_nodes)
        adj_matrix = np.zeros((num_nodes, num_nodes))
        if not joint_nodes:
            # 如果没有找到关节节点，返回空的邻接矩阵
            return adj_matrix

        for node in joint_nodes:
            children = list(robot_graph.successors(node))[0] if list(robot_graph.successors(node)) else None
            parent = list(robot_graph.predecessors(node))[0] if list(robot_graph.predecessors(node)) else None
            parent_index = link_nodes.index(parent) if parent in link_nodes else -1
            child_index = link_nodes.index(children) if children in link_nodes else -1
            if parent_index >= 0 and child_index >= 0:
                adj_matrix[parent_index, child_index] = 1
                adj_matrix[child_index, parent_index] = 1
        return adj_matrix

    def extract_node_features(self, robot_graph,pos_rot):
        # 在这里实现提取节点特征的逻辑
        # 请根据您的图结构自行设计节点特征的提取方法
        # 返回节点特征的 numpy 数组.

        link_features = []
        links = [node_info for _, node_info in robot_graph.nodes(data='info') if isinstance(node_info, RobotLink)]
        for node_name, link in zip(pos_rot.keys(), links):
            world_pos, world_rot = pos_rot[node_name]
            parent_nodes = list(robot_graph.predecessors(node_name))
            parent_pos, parent_rot = pos_rot[node_name]
            

            if parent_nodes:
                parent_node_name = list(robot_graph.predecessors(node_name))[0]
                parent_link_info = robot_graph.nodes[parent_node_name]['info']
                world_joint_axis = quaternion.rotate_vectors(parent_rot, parent_link_info.axis)
                # world_joint_axis = quaternion.rotate_vectors(world_rot, link.joint_axis)
                label_vec = np.zeros(len(self.all_labels))
                # print("self.all_labels",self.all_labels)
                label_vec[self.all_labels.index(link.label)] = 1
        
                link_features.append(np.array([
                        *featurize_link(link),
                        *world_pos,
                        *quaternion_coords(world_rot),
                        *world_joint_axis,
                        *label_vec]))
            else:


                data = [0.0, 0.0, 1.0]
                label_vec = np.zeros(len(self.all_labels))
                label_vec[self.all_labels.index(link.label)] = 1

                link_features.append(np.array([
                        *featurize_link(link),
                        *world_pos,
                        *quaternion_coords(world_rot),
                        *np.array(data, dtype=float),
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
    
    def pad_graph(self, adj_matrix, features, max_nodes):
        real_size = features.shape[0]

        # add blank nodes
        adj_matrix = self.pad(adj_matrix, (max_nodes, max_nodes))
        features = self.pad(features, (max_nodes, features.shape[1]))

        # create mask
        masks = np.array([True if i < real_size else False for i in range(max_nodes)])

        return adj_matrix, features, masks
    
    def pad(self, array, shape):
        """
        array: Array to be padded
        reference: Reference array with the desired shape
        offsets: list of offsets (number of elements must be equal to the dimension of the array)
        """
        # Create an array of zeros with the reference shape
        result = np.zeros(shape)
        if len(shape) == 1:
            result[:array.shape[0], :] = array # ERROR: why result is 2d
        elif len(shape) == 2:
            result[:array.shape[0], :array.shape[1]] = array
        else:
            raise Exception('only 1 and 2d supported for now')
        return result