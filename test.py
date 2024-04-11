import os
import time
# 获取当前时间
current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

# 创建相对路径
relative_path = os.path.join("mjcf_model", current_time)
print(relative_path)
# 将相对路径转换为绝对路径
absolute_path = os.path.abspath(relative_path)
print(absolute_path)