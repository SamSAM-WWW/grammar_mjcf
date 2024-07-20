import numpy as np

def read_obj_file(file_path):
    """
    Read an OBJ file and extract vertex positions.
    
    Parameters:
        file_path (str): Path to the OBJ file.
        
    Returns:
        vertices (np.array): Array of vertex positions.
    """
    vertices = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                x, y, z = map(float, parts[1:])
                vertices.append([x, y, z])
    
    return np.array(vertices)

def obj_to_heightmap(vertices, width, length, horizontal_scale, vertical_scale):
    """
    Convert OBJ vertices to a height map.
    
    Parameters:
        vertices (np.array): Array of vertex positions.
        width (int): Width of the height map.
        length (int): Length of the height map.
        horizontal_scale (float): Horizontal scale.
        vertical_scale (float): Vertical scale.
    
    Returns:
        height_map (np.array): 2D array representing the height map.
    """
    height_map = np.zeros((width, length), dtype=np.float32)
    
    for vertex in vertices:
        x, y, z = vertex
        i = int(x / horizontal_scale)
        j = int(y / horizontal_scale)
        if 0 <= i < width and 0 <= j < length:
            height_map[i, j] = z / vertical_scale
    
    return height_map

def save_heightmap_to_txt(height_map, file_path):
    """
    Save the height map to a TXT file.
    
    Parameters:
        height_map (np.array): 2D array representing the height map.
        file_path (str): Path to the TXT file.
    """
    np.savetxt(file_path, height_map, fmt='%.5f')
    
# 使用示例
file_path = 'D:\pythoncode\grammar_mjcf\objs\\xiei_ao.obj'  # 替换为实际的OBJ文件路径
vertices = read_obj_file(file_path)

# 定义地形参数
width = 256
length = 256
horizontal_scale = 0.1
vertical_scale = 0.1

height_map = obj_to_heightmap(vertices, width, length, horizontal_scale, vertical_scale)

# 保存高度图到TXT文件
txt_file_path = 'D:\pythoncode\grammar_mjcf\objs\\heightmap.txt'  # 替换为实际的TXT文件路径
save_heightmap_to_txt(height_map, txt_file_path)

print(f"Height map saved to {txt_file_path}")