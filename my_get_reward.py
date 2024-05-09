from uni import UniSimulator
import os
import shutil
import wandb
import gin
from uni.utils import gin_util
from uni.utils import rng
from uni.rl.util import rl_evaluate
from uni.rl.wrappers.timeout_wrapper import TimeoutWrapper
import matplotlib.pyplot as plt
import time

class MyUNI(UniSimulator):
    def simulate(self, train_t:int=20000000):
        rng.seed(self.seed)

        save_period = 100000
        t = self.alg.load()
        last_save = (t // save_period) * save_period
        # Train 
        if train_t > 0:
            self.alg.env.init_scene()
            with open('log.txt', 'a+') as f:
                f.write(f'start: {time.asctime(time.localtime(time.time()))}\n')
                while True:
                    t = self.alg.step()
                    if (t - last_save) >= save_period:
                        data = self.alg.evaluate()
                        med_re = data['median_reward']
                        f.write(f'{med_re}\n')
                        last_save = t
                    if t - self.t > train_t:
                        print(t)
                        self.t = t
                        break
            self.alg.save()


if __name__ == '__main__':
    uni = UniSimulator('mjcf_model/tests/test8','/home/ps/pan1/files/Sam/grammar_mjcf-master/my_config/grammar.gin')
    uni.simulate(40000000)
    uni.close()
    # UniSimulator.visual('mjcf_model/tests/test8','/home/ps/pan1/files/Sam/grammar_mjcf-master/my_config/grammar.gin')
    # UniSimulator.terrain_visual('/home/ps/pan1/files/Sam/grammar_mjcf-master/mjcf_model/2024-04-25_10-23-29', mode='test')