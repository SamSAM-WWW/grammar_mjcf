# Grammar-mjcf
Commands were tested on Ubuntu 20.04.
Python 3.7
先配置Isaac环境
# 环境有两个需要配一个是Isaac Gym 一个是Isaac Gym Envs

配置整体来说是比较简单的，遇到的几个问题都能看教程解决

[Isaac Gym环境安装和四足机器人模型的训练-CSDN博客](https://blog.csdn.net/weixin_44061195/article/details/131830133?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2~default~YuanLiJiHua~Position-2-131830133-blog-124605383.235^v38^pc_relevant_sort&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~YuanLiJiHua~Position-2-131830133-blog-124605383.235^v38^pc_relevant_sort&utm_relevant_index=5)

1.在官网下载最新的文件包[Isaac Gym - Preview Release](https://developer.nvidia.com/isaac-gym)，注意需要登陆。

其中assets是模型材料位置
其中docs是说明网站位置
其中python是演示程序位置
可以根据说明文档安装方式安装
这里只介绍其中conda安装的方法

```
# 在文件根目录里运行
./create_conda_env_rlgpu.sh
# 激活环境
conda activate rlgpu
# 正常情况下这时候可以运行实例程序/isaacgym/python/examples/joint_monkey.py
python joint_monkey.py
# 可以通过--asset_id命令控制显示的模型
python joint_monkey.py --asset_id=6

```

到这里IsaacGym就安装好了

### 根据教程配置Isaac Gym 

`./create_conda_env_rlgpu.sh`要等很久是正常的

### 无论何时遇到 这个很关键

`# 出现这样的报错
ImportError: libpython3.7m.so.1.0: cannot open shared object file: No such file or directory`

需要`sudo apt install libpython3.7`或者`export LD_LIBRARY_PATH=/home/ps/anaconda3/envs/rlgpu/lib`尝试一下就行 大概率后者设置路径有效









如果报以下错误是因为模型文件URDF文件中mesh文件的地址出错，找不到模型文件导致的。建议可以直接写绝对地址。

```
[Error] [carb.gym.plugin] Failed to resolve visual mesh '/isaacgym/Quadruped/legged_gym-master/resources/robots/meshes/anymal/trunk.stl'

```

### 2. IsaacGym基础训练环境安装

GitHub上下载好 进文件内

```
conda activate rlgpu
pip install -e .
```

有几个装不上的多试几次，重启终端、电脑

这里装完之后pytorch好像得重装



Isaac gym envs也是根据教程 但是训练模型时候遇到了问题，训练的gui一闪而过之后`run time error nvrtc: invalid value for --gpu-architecture(-arch)`

尝试重装pytorch可以 然后重新设置一下上面的那个路径

pytorch 1.12 cuda11.6

到train.py 的文件夹路径内训练

```
python train.py task=Ant
# 不显示动画只训练
python train.py task=Ant headless=True
# 测试训练模型的效果，num_envs是同时进行训练的模型数量
python train.py task=Ant checkpoint=runs/Ant/nn/Ant.pth test=True num_envs=64

```











其他python包安装
`cd uni`
`pip install -e.`
直接在我的文件夹下nlimb uni 文件夹下面pip install -e.应该就行

装好了就可以from uni import UniSimulator

先创建一个实例化，后面每次调.simulate就行



一些可能用到的包见requirements.txt 缺什么就装什么 有gpu就安装gpu版本的torch 和 cuda  不过这些内容应该在Isaac安装时已经解决


每次跑之前可以把exps这个文件夹删一下



