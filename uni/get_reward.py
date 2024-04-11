import os
import shutil
import wandb
import gin
from uni.utils import gin_util
from uni.utils import rng
from uni.rl.util import rl_evaluate
from uni.rl.wrappers.timeout_wrapper import TimeoutWrapper

class UniSimulator():
    def __init__(self, folder:str, config_path:str='/home/ps/pan1/files/ypf/srl/configs/grammar.gin') -> None:
        wandb.init(mode='disabled')
        gin_util.add_pytorch_external_configurables()
        gin_util.load_config(config_path, finalize=False)
        config = gin_util.get_config_dict()
        config['nlimb.NLIMB.xml_root'] = folder
        gin_util.apply_bindings_from_dict(config)
        self.logdir = gin.query_parameter('rl.train.logdir')
        if os.path.exists(self.logdir):
            shutil.rmtree(self.logdir)
        os.makedirs(self.logdir, exist_ok=True)
        self.seed = gin.query_parameter('rl.train.seed')
        self.alg = gin.query_parameter('rl.train.algorithm').configurable.wrapped(self.logdir)
        self.t = self.alg.load()
        self.folder = folder
        self.config_path = config_path

    def simulate(self, train_t:int=20000000):
        rng.seed(self.seed)

        # Train 
        if train_t > 0:
            self.alg.env.init_scene()
            while True:
                t = self.alg.step()
                if t - self.t > train_t:
                    print(t)
                    self.t = t
                    break
            self.alg.save()
        
        data = self.alg.evaluate()
        
        return data
    
    @staticmethod
    def visual(folder:str, config_path:str='/home/ps/pan1/files/ypf/srl/configs/grammar.gin'):
        rng.seed(0)
        num_envs = len(os.listdir(folder))
        assert num_envs > 0, f'No environments found in {folder}'
        print(f'Found {num_envs} environments in {folder}')
        wandb.init(mode='disabled')
        gin_util.add_pytorch_external_configurables()
        gin_util.load_config(config_path, finalize=False)
        config = gin_util.get_config_dict()
        config['envs.IsaacMixedXMLEnv.num_envs'] = num_envs
        config['envs.IsaacMixedXMLEnv.spacing'] = (0., 0.025, 1.)
        config['envs.IsaacMixedXMLEnv.create_eval_sensors'] = True

        config['nlimb.NLIMB.xml_root'] = folder
        gin_util.apply_bindings_from_dict(config)
        logdir = gin.query_parameter('rl.train.logdir')

        alg = gin.query_parameter('rl.train.algorithm').configurable.wrapped(logdir)
        alg.load()
        pi = alg.alg.pi
        env = alg.alg.env
        env.finalize_obs_norm()
        env = TimeoutWrapper(env, alg.alg.eval_max_episode_length)
        env.init_scene(test=True)
        env.create_viewer()
        rl_evaluate(env, pi, nepisodes=alg.env.num_envs, t=alg.t, record_viewer=False,
                    outdir=logdir, num_recording_envs=num_envs)
        alg.close()
    
    def save(self):
        self.alg.save()
    
    def close(self):
        self.alg.close()

if __name__ == '__main__':
    uni = UniSimulator('/home/ps/pan1/files/Sam/grammar_mjcf-master/mjcf_model/test')
    uni.simulate(20000000)
    uni.close()
    UniSimulator.visual('/home/ps/pan1/files/Sam/grammar_mjcf-master/mjcf_model/test')