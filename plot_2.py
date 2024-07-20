import hashlib
import os
import csv
import matplotlib.pyplot as plt

def calculate_hash(xml_content):
    # 计算内容的哈希值
    hash_value = hashlib.sha256(xml_content.encode()).hexdigest()
    return hash_value


def calculate_hash_without_first_line(xml_file):
    # 读取XML文件的内容
    with open(xml_file, 'r') as file:
        xml_content = file.read()

    # 移除第一行
    xml_content_without_first_line = '\n'.join(xml_content.split('\n')[1:])

    # 计算移除第一行后的XML文件的哈希值
    hash_without_first_line = calculate_hash(xml_content_without_first_line)

    return hash_without_first_line
# 调用函数计算XML文件的哈希值

def process_xml_files(folder_path):
    # 存储哈希值和对应的文件列表
    hash_to_files = {}

    # 遍历文件夹
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.xml'):
                # 构建文件的完整路径
                file_path = os.path.join(root, file_name)
                
                # 计算文件的哈希值（不含第一行）
                hash_value = calculate_hash_without_first_line(file_path)

                # 更新哈希值对应的文件列表
                if hash_value in hash_to_files:
                    hash_to_files[hash_value].append(file_path)
                else:
                    hash_to_files[hash_value] = [file_path]

    return hash_to_files

# 调用函数处理文件夹中的XML文件
folder_path = "D:\pythoncode\grammar_mjcf\mjcf_model\\2024-05-05_19-13-41"
hash_to_files = process_xml_files(folder_path)

# 输出哈希值和对应的文件列表
for hash_value, file_list in hash_to_files.items():
    print(f"Hash Value: {hash_value}")
    print("Files:")
    for file_path in file_list:
        print(f"- {file_path}")


def find_reward_for_xml_file(csv_file, xml_file_name):
    reward = None

    # 遍历 CSV 文件
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 提取出 XML 文件名
            file_name = row['xml_out_path'].split('/')[-1]
            # 找到对应的行
            if file_name == xml_file_name:
                reward = row['reward']
                break

    return reward

# CSV 文件路径
csv_file = "D:\pythoncode\grammar_mjcf\mjcf_model\\2024-05-05_19-13-41\design_rewards.csv"
# 哈希值
hash_value = "0a59e0624e92adbb4e7632933f5607a05eb50c0999cb1022ac14f16dba9df7b6"

# 获取 hash 对应的 XML 文件列表
xml_files = hash_to_files.get(hash_value, [])


reward_list_best = []
# 遍历每个 XML 文件
for xml_file in xml_files:
    # 提取出 XML 文件名
    xml_file_name = os.path.basename(xml_file)
    # 查找 XML 文件名对应的 reward
    reward = find_reward_for_xml_file(csv_file, xml_file_name)
    if reward is not None:
        print(f"The reward for XML file {xml_file_name} is: {reward}")
        reward_list_best.append(reward)
    else:
        print(f"No reward found for XML file {xml_file_name}")


# CSV 文件路径
csv_file = "D:\pythoncode\grammar_mjcf\mjcf_model\\2024-05-05_19-13-41\design_rewards.csv"
# 哈希值
hash_value = "0053a60132247c19bec0ef04e1a3048f3adc7b9f647e334b7d86e775583d5f7e"

# 获取 hash 对应的 XML 文件列表
xml_files = hash_to_files.get(hash_value, [])


reward_list_me = []
# 遍历每个 XML 文件
for xml_file in xml_files:
    # 提取出 XML 文件名
    xml_file_name = os.path.basename(xml_file)
    # 查找 XML 文件名对应的 reward
    reward = find_reward_for_xml_file(csv_file, xml_file_name)
    if reward is not None:
        print(f"The reward for XML file {xml_file_name} is: {reward}")
        reward_list_me.append(reward)
    else:
        print(f"No reward found for XML file {xml_file_name}")


# CSV 文件路径
csv_file = "D:\pythoncode\grammar_mjcf\mjcf_model\\2024-05-05_19-13-41\design_rewards.csv"
# 哈希值
hash_value = "34e0e2f883fdde9aa5ff14e4303b2d7d40d33d6f2557cda364c642bd8b62e0c7"

# 获取 hash 对应的 XML 文件列表
xml_files = hash_to_files.get(hash_value, [])


reward_list_wo = []
# 遍历每个 XML 文件
for xml_file in xml_files:
    # 提取出 XML 文件名
    xml_file_name = os.path.basename(xml_file)
    # 查找 XML 文件名对应的 reward
    reward = find_reward_for_xml_file(csv_file, xml_file_name)
    if reward is not None:
        print(f"The reward for XML file {xml_file_name} is: {reward}")
        reward_list_wo.append(reward)
    else:
        print(f"No reward found for XML file {xml_file_name}")

reward_list_best = [float(reward) for reward in reward_list_best]
reward_list_me = [float(reward) for reward in reward_list_me]
reward_list_wo = [float(reward) for reward in reward_list_wo]
# Plotting the boxplot
# Plotting the boxplots
plt.figure(figsize=(10, 5))

# Specify positions for the boxplots
positions = [1, 2, 3]

# Plot each boxplot with specified positions
plt.boxplot(reward_list_wo, positions=[positions[0]], patch_artist=True, boxprops=dict(facecolor='blue'), labels=['wo'])
plt.boxplot(reward_list_me, positions=[positions[1]], patch_artist=True, boxprops=dict(facecolor='green'), labels=['me'])
plt.boxplot(reward_list_best, positions=[positions[2]], patch_artist=True, boxprops=dict(facecolor='orange'), labels=['best'])

# Set title and labels
plt.title('Boxplot of Rewards')
plt.ylabel('Reward')

# Set x-axis ticks and labels
plt.xticks(positions, ['worst design', 'medium design', 'best design'])

# Show the plot
plt.show()