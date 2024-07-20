import numpy as np
import matplotlib.pyplot as plt
import trimesh
from scipy.interpolate import griddata

# 加载STL文件
mesh = trimesh.load('objs/big_terrain.STL')

# 提取顶点数据
vertices = mesh.vertices

# 提取Z坐标作为高度数据
heights = vertices[:, 2]

# 创建一个网格
x = np.linspace(np.min(vertices[:, 0]), np.max(vertices[:, 0]), 256)
y = np.linspace(np.min(vertices[:, 1]), np.max(vertices[:, 1]), 256)
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
np.savetxt('height_field.txt', Z.T, fmt='%.6f', header='Height Field Data', comments='')