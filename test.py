import os
import csv

def save_to_csv(data, filename):
    # 检查文件是否存在
    file_exists = os.path.isfile(filename)

    # 打开 CSV 文件，使用不同的模式（追加或新建）
    with open(filename, mode='a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)
        # 如果文件是新建的，则写入列标题
        if not file_exists:
            writer.writerow(['xml_out_path', 'hash', 'reward'])
        # 写入数据
        for row in data:
            writer.writerow(row)

# 使用示例
data_to_save = [['path1', 'hash1', 10], ['path2', 'hash2', 20], ['path3', 'hash3', 30]]
save_to_csv(data_to_save, 'design_rewards.csv')