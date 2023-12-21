from enum import Enum
from typing import List, Set, Dict, Union
import numpy as np

# Define Enumerations
class LinkShape(Enum):
    NONE = 0
    CAPSULE = 1
    CYLINDER = 2

class JointType(Enum):
    NONE = 0

class JointControlMode(Enum):
    POSITION = 0

# Define Scalars, Vectors, and Quaternions
Scalar = float
Vector3 = np.ndarray  # Assuming you're using NumPy for vectors
Quaternion = np.ndarray  # Assuming you're using NumPy for quaternions

# Define Indices
NodeIndex = int
EdgeIndex = int

class NodeAttributes:
    def __init__(self, label: str = "", shape: LinkShape = LinkShape.NONE, length: Scalar = 1.0,
                 radius: Scalar = 0.05, density: Scalar = 1.0, friction: Scalar = 0.9, base: bool = False,
                 require_label: str = ""):
        self.label = label
        self.shape = shape
        self.length = length
        self.radius = radius
        self.density = density
        self.friction = friction
        self.base = base

        self.require_label = require_label

class Node:
    def __init__(self, name: str, attrs: NodeAttributes):
        self.name = name
        self.attrs = attrs

class EdgeAttributes:
    def __init__(self, id: str = "", label: str = "", joint_type: JointType = JointType.NONE,
                 joint_pos: Scalar = 1.0, joint_rot: Quaternion = Quaternion.identity(),
                 joint_axis: Vector3 = Vector3.unit_z(), joint_kp: Scalar = 0.01, joint_kd: Scalar = 0.5,
                 joint_torque: Scalar = 1.0, joint_lower_limit: Scalar = 0.0, joint_upper_limit: Scalar = 0.0,
                 joint_control_mode: JointControlMode = JointControlMode.POSITION, scale: Scalar = 1.0,
                 mirror: bool = False,  require_label: str = ""):
        self.id = id
        self.label = label
        self.joint_type = joint_type
        self.joint_pos = joint_pos
        self.joint_rot = joint_rot
        self.joint_axis = joint_axis
        self.joint_kp = joint_kp
        self.joint_kd = joint_kd
        self.joint_torque = joint_torque
        self.joint_lower_limit = joint_lower_limit
        self.joint_upper_limit = joint_upper_limit
        self.joint_control_mode = joint_control_mode
        self.scale = scale
        self.mirror = mirror
        self.require_label = require_label

class Edge:
    def __init__(self, head: NodeIndex, tail: NodeIndex, attrs: EdgeAttributes):
        self.head = head
        self.tail = tail
        self.attrs = attrs

class Subgraph:
    def __init__(self, name: str, nodes: Set[NodeIndex], edges: Set[EdgeIndex],
                 node_attrs: NodeAttributes, edge_attrs: EdgeAttributes):
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.node_attrs = node_attrs
        self.edge_attrs = edge_attrs

class Graph:
    def __init__(self, name: str, nodes: List[Node], edges: List[Edge], subgraphs: List[Subgraph]):
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.subgraphs = subgraphs

class GraphMapping:
    def __init__(self, node_mapping: List[NodeIndex], edge_mapping: List[List[EdgeIndex]]):
        self.node_mapping = node_mapping
        self.edge_mapping = edge_mapping

class Rule:
    def __init__(self, name: str, lhs: Graph, rhs: Graph, common: Graph,
                 common_to_lhs: GraphMapping, common_to_rhs: GraphMapping):
        self.name = name
        self.lhs = lhs
        self.rhs = rhs
        self.common = common
        self.common_to_lhs = common_to_lhs
        self.common_to_rhs = common_to_rhs


node_attrs = NodeAttributes(label="my_node", shape=LinkShape.CAPSULE, length=2.0)

# 创建 Node 实例
node = Node(name="node_1", attrs=node_attrs)