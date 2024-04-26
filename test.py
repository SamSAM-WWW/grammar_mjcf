import torch
from torch.utils.tensorboard import SummaryWriter
from Net import GNN, Net
num_channels = 32
max_nodes = 32
in_channels = 32
hidden_channels = 64
out_channels = 16
num_outputs = 10
# 创建一个示例输入张量
input_tensor = torch.randn(1, num_channels, max_nodes)

# 创建一个示例邻接矩阵张量
adj_tensor = torch.randn(1, max_nodes, max_nodes)

# 创建一个TensorBoard写入器对象
writer = SummaryWriter('logs')


# 创建一个Net模型实例
net_model = Net(max_nodes, num_channels, num_outputs)
# 将Net模型的图结构写入TensorBoard
writer.add_graph(net_model, (input_tensor, adj_tensor))

# 关闭TensorBoard写入器
writer.close()