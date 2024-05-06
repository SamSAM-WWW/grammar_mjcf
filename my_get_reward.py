from uni import UniSimulator

import matplotlib.pyplot as plt
def update_controller(uni):
    return uni.simulate(100000)

if __name__ == '__main__':
    reward_list = []
    xml_name = 'xxxxx.xml'
    uni = UniSimulator('mjcf_model/tests/test8','/home/ps/pan1/files/Sam/grammar_mjcf-master/my_config/grammar.gin')
    
    for i in range(400):
        reward_dict = update_controller(uni)
        reward = reward_dict['median_reward'] #reward = {"xmlrobot_0.xml": 76, "xmlrobot_1.xml": 73}
        val = reward[xml_name]
        reward_list.append(val)

    uni.close()
    print('reward list is ',reward_list)
    plt.plot(reward_list)
    plt.title('Reward')
    # 生成 x 轴刻度的位置和标签
step_size = 100000
x_ticks = [i * step_size for i in range(len(reward_list))]
x_labels = [f'{i * step_size // 100000}' for i in range(len(reward_list))]

# 绘制图表
plt.plot(reward_list)
plt.title('Reward')
plt.xlabel('Steps (x100000)')
plt.ylabel('Value')
plt.xticks(x_ticks, x_labels)  # 设置 x 轴刻度
plt.grid(True)
plt.tight_layout()
plt.show()
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

    # uni = UniSimulator('mjcf_model/tests/test8','/home/ps/pan1/files/Sam/grammar_mjcf-master/my_config/grammar.gin')
    # uni.simulate(40000000)
    # uni.close()
    # UniSimulator.visual('mjcf_model/tests/test8','/home/ps/pan1/files/Sam/grammar_mjcf-master/my_config/grammar.gin')
    # UniSimulator.terrain_visual('/home/ps/pan1/files/Sam/grammar_mjcf-master/mjcf_model/2024-04-25_10-23-29', mode='test')