import hashlib
def calculate_hash_without_first_line(xml_file):
    # 读取XML文件的内容
    with open(xml_file, 'r') as file:
        xml_content = file.read()

    # 移除第一行
    xml_content_without_first_line = '\n'.join(xml_content.split('\n')[1:])

    # 计算移除第一行后的XML文件的哈希值
    hash_without_first_line = calculate_hash(xml_content_without_first_line)
    return hash_without_first_line
def calculate_hash(xml_content):
    # 计算内容的哈希值
    hash_value = hashlib.sha256(xml_content.encode()).hexdigest()
    return hash_value
    
hash_val = calculate_hash_without_first_line(xml_file='mjcf_model\\xmlrobot_8_symm.xml')
print(hash_val)