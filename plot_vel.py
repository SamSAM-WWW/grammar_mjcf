import matplotlib.pyplot as plt
import pandas as pd

# 读取 CSV 文件
file_path = "D:\pythoncode\grammar_mjcf\mjcf_model\\rule7\\root_vel_m.csv"
data_0 = pd.read_csv(file_path)
vel_data = data_0['root_vel_x']
mean_val = vel_data.mean()
print(mean_val)
plt.figure(figsize=(10, 5))
plt.plot(vel_data, label='worst design')

# 添加标题和标签
plt.title('Velocity')
plt.xlabel('Time')
plt.ylabel('Velocity')

# 添加图例
plt.legend()
plt.show()