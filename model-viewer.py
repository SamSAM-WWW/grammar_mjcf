# ------- 来自于mujoco150在win+py3.9下的矫情的要求 --------
# 手动添加mujoco路径
import os
import time
from getpass import getuser

user_id = getuser()
os.add_dll_directory(f"C://Users//{user_id}//.mujoco//mujoco200//bin")
os.add_dll_directory(f"C://Users//{user_id}//.mujoco//mujoco-py-2.0.2.0//mujoco_py")
# -------------------------------------------------------


import sys

from mujoco_py import MjSim, MjViewer, load_model_from_path

model_path = sys.argv[1]
print(model_path)
model = load_model_from_path(model_path)
sim = MjSim(model)
viewer = MjViewer(sim)

for i in range(15000):
    sim.step()
    viewer.render()
