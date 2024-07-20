import matplotlib.pyplot as plt
import pandas as pd

# 读取 CSV 文件
file_path = "D:\pythoncode\grammar_mjcf\mjcf_model\\rule7/root_rel_height_m.csv"
data_0 = pd.read_csv(file_path)

# 读取 CSV 文件
file_path = "D:\pythoncode\grammar_mjcf\mjcf_model\\rule7/root_rel_height.csv"
data_1 = pd.read_csv(file_path)

# 提取高度数据
height_data_0 = data_0['root_rel_height']
height_data_1 = data_1['root_rel_height']

# # 提取高度数据的子集
# height_data_0_sub = data_0['root_rel_height'][:int(len(data_0)*7/8)]
# height_data_1_sub = data_1['root_rel_height'][:int(len(data_1)*1/4)]

# 提取高度数据的子集
height_data_0_sub = data_0['root_rel_height'][:int(len(data_0))]
height_data_1_sub = data_1['root_rel_height'][:int(len(data_1))]
plt.figure(figsize=(10, 5))







plt.figure(figsize=(10, 5))
# 创建图表并绘制数据
plt.plot(height_data_0_sub, label='worst design')
plt.plot(height_data_1_sub, label='best design')

# 添加标题和标签
plt.title('Height Data Comparison')
plt.xlabel('Time')
plt.ylabel('Height')

# 添加图例
plt.legend()

# 显示图表
plt.show()
# 计算标准差

# 计算均值和标准差
mean_0 = height_data_0_sub.mean()
mean_1 = height_data_1_sub.mean()
std_deviation_0 = height_data_0_sub.std()
std_deviation_1 = height_data_1_sub.std()

# # 计算变异系数
cv_0 = std_deviation_0 / mean_0
cv_1 = std_deviation_1 / mean_1

print("变异系数 data_0 子集:", cv_0)
print("变异系数 data_1 子集:", cv_1)
print((cv_0 - cv_1)/cv_1)

print("标准差 data_0 子集:", std_deviation_0)
print("标准差 data_1 子集:", std_deviation_1)
print((std_deviation_0 - std_deviation_1)/std_deviation_1)

# 设置柱状图参数
labels = ['worst design', 'best design']
means = [mean_0, mean_1]
stds = [std_deviation_0, std_deviation_1]
x = range(len(labels))

plt.figure(figsize=(4, 5))
# 绘制柱状图
plt.bar(x, means, yerr=stds, tick_label=labels, align='center', alpha=0.7, ecolor='black', capsize=10, color=['blue', 'green'])
plt.ylabel('Value')
plt.title('Mean and Standard Deviation Comparison')

# 显示图例
plt.legend(['Mean', 'Standard Deviation'])

# 显示图表
plt.show()