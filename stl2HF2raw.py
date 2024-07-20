import numpy as np
import matplotlib.pyplot as plt
import trimesh
from scipy.interpolate import griddata

import os
import numpy as np
import matplotlib.pyplot as plt
import trimesh
from scipy.interpolate import griddata


#80160
def process_stl_80160(file_name,bili):
    # 创建文件夹 stl2hight 如果它不存在
    os.makedirs('stl2hight', exist_ok=True)

    # 构建输入和输出文件名
    input_file = os.path.join('stl2hight', f'{file_name}.stl')
    output_file = os.path.join('stl2hight', f'{file_name}.txt')
    output_file_8080 = os.path.join('stl2hight', f'{file_name}_8080.txt')

    # 检查STL文件是否存在
    if not os.path.exists(input_file):
        print(f"Error: {input_file} 文件不存在")
        return

    # 加载STL文件
    mesh = trimesh.load(input_file)

    # 提取顶点数据
    vertices = mesh.vertices

    # 提取Z坐标作为高度数据
    heights = vertices[:, 2] * int(bili)

    # 创建一个网格
    x = np.linspace(np.min(vertices[:, 0]), np.max(vertices[:, 0]), 80)
    y = np.linspace(np.min(vertices[:, 1]), np.max(vertices[:, 1]), 160)
    X, Y = np.meshgrid(x, y)

    # 使用scipy进行插值
    Z = griddata((vertices[:, 0], vertices[:, 1]), heights, (X, Y), method='linear')

    # 处理插值后的NaN值
    nan_mask = np.isnan(Z)
    Z[nan_mask] = np.interp(np.flatnonzero(nan_mask), np.flatnonzero(~nan_mask), Z[~nan_mask])

    # 绘制高度图
    plt.imshow(Z.T, extent=(np.min(y), np.max(y), np.min(x), np.max(x)), origin='lower', cmap='terrain')
    plt.colorbar()
    plt.title('Height Field')
    plt.xlabel('Y')
    plt.ylabel('X')
    plt.show()

    # 保存高度图数据到txt文件
    np.savetxt(output_file, Z.T, fmt='%.6f', header='Height Field Data', comments='')

    # 去除右边的80列，得到80x80的数据
    Z_80x80 = Z[:-80, :]
    # 保存80x80高度图数据到新的txt文件
    np.savetxt(output_file_8080, Z_80x80.T, fmt='%.6f', header='Height Field Data 80x80', comments='')
file_name = input("请输入文件名（不带后缀）：")
bili = input("请输入倍率：")
print("export to D:\pythoncode\grammar_mjcf\stl2hight",f'{file_name}.txt')
process_stl_80160(file_name,bili)