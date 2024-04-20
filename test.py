# import numpy as np
# from torch.utils.tensorboard import SummaryWriter

# # 创建一个TensorBoard的SummaryWriter对象
# writer = SummaryWriter()

# # 从文件中读取数据
# file_path = "data.txt"
# predicted_rewards = []
# rewards = []

# with open(file_path, 'r') as file:
#     for line in file:
#         parts = line.strip().split(', ')
#         for part in parts:
#             if part.startswith('predicted_reward'):
#                 predicted_rewards.append(float(part.split('=')[1]))
#             elif part.startswith('reward'):
#                 rewards.append(float(part.split('=')[1]))

# # 转换为NumPy数组
# predicted_rewards = np.array(predicted_rewards)
# rewards = np.array(rewards)

# # 计算逐步增加样本后的均方根误差（RMSE）并将其写入TensorBoard事件文件
# for i in range(1, len(predicted_rewards) + 1):
#     rmse = np.sqrt(np.mean((predicted_rewards[:i] - rewards[:i]) ** 2))
#     writer.add_scalar('Metrics/RMSE', rmse, global_step=i)

# # 关闭SummaryWriter对象
# writer.close()





# import numpy as np
# from sklearn.metrics import mean_squared_error
# import random
# from torch.utils.tensorboard import SummaryWriter

# # 初始化列表来存储reward和selected_reward
# reward_list = []
# selected_reward_list = []
# writer = SummaryWriter()
# # 假设从某处获取了数据并将其添加到列表中
# for epoch in range(1000):
#     reward = random.random()
#     selected_reward = random.random()
#     reward_list.append(reward)
#     selected_reward_list.append(selected_reward)

#     # 转换列表为NumPy数组
#     reward_array = np.array(reward_list)
#     selected_reward_array = np.array(selected_reward_list)

#     # 计算RMSE
#     rmse = np.sqrt(mean_squared_error(selected_reward_array, reward_array))

#     # 将RMSE写入TensorBoard
#     writer.add_scalar("RMSE", rmse, epoch)
#     writer.add_scalar("Predicted Reward", selected_reward, epoch)
#     writer.add_scalar("Actual Reward", reward, epoch)
#     writer.add_scalar("Reward Difference", reward - selected_reward, epoch)




import numpy as np
from torch.utils.tensorboard import SummaryWriter
import csv

# 创建一个TensorBoard的SummaryWriter对象
writer = SummaryWriter()
# 提取数据
csv_file_path = "data.csv"  # 请替换成你的CSV文件路径


# 数据
rewards = [93.1, 78.7, 76.4, 50.11, 76.62, 49.16, 83.05, 80, 50.1, 38.91, 79.87, 66.59, 48.27, 78.8, 77.45, 52.21, 77.99, 77.89]
predicted_rewards = [10.4, 91.96, 86.87, 83.26, 74.42, 72.07, 67.75, 73.99, 71.2, 73.44, 66.6, 68.43, 66.2, 64.81, 66.63, 66.09, 68.14, 69.44]

with open(csv_file_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        rewards.append(float(row['reward']))
        predicted_rewards.append(float(row['predict_reward']))



# 计算逐步增加样本后的均方根误差（RMSE）并将其写入TensorBoard事件文件
for i in range(1, len(rewards) + 1):
    rmse = np.sqrt(np.mean((np.array(predicted_rewards[:i]) - np.array(rewards[:i]))**2))
    writer.add_scalar('Metrics/RMSE', rmse, global_step=i)

# 关闭SummaryWriter对象
writer.close()






