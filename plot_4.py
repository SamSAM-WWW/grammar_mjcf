from matplotlib import pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (4,5)
x = range(2)
x_label=['Traditional Method','Our Method']
plt.xticks(x, x_label,fontproperties='Times New Roman')  # 绘制x刻度标签
# data = [17.33, 87.52, 141.32]
data = [138.24, 52.61]
plt.title("Training duration (Hours)",fontproperties='Times New Roman')
plt.grid(axis="y", c='#d2c9eb', linestyle = '--',zorder=0)
bars = plt.bar(x, data, color=["#92a6be", "#c48d60"], width=0.3, zorder=3)

#plt.bar(x, data ,color="green")
for bar, value in zip(bars, data):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value}', ha='center', va='bottom', fontproperties='Times New Roman')
plt.show()