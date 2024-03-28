import os
import wandb
import gin
import copy
from uni.utils import gin_util
from uni.rl.util import rl_evaluate
from uni.rl.wrappers.timeout_wrapper import TimeoutWrapper
from uni.utils import rng

class UniSimulator():
    def __init__(self) -> None:
        wandb.init(mode='disabled')
        gin_util.add_pytorch_external_configurables()
        gin_util.load_config('/home/ps/pan1/files/ypf/nlimb2/configs/grammar.gin', finalize=False)
        self.logdir = gin.query_parameter('rl.train.logdir')
        os.makedirs(self.logdir, exist_ok=True)
        self.seed = gin.query_parameter('rl.train.seed')

    def simulate(self, folder:str, train_t:int=20000000, record:bool=False):
        # Set xml root
        config = gin_util.get_config_dict()
        config['nlimb.NLIMB.xml_root'] = folder
        gin_util.apply_bindings_from_dict(config)
        # Train 
        if train_t > 0:
            rng.seed(self.seed)
            alg = gin.query_parameter('rl.train.algorithm').configurable.wrapped(self.logdir)
            t0 = alg.load()
            while True:
                t = alg.step()
                if t - t0 > train_t:
                    break
            alg.save()
            alg.close()
        # Evaluate
        num_envs = len(os.listdir(folder))
        assert num_envs > 0, f'No environments found in {folder}'
        print(f'Found {num_envs} environments in {folder}')
        
        config = gin_util.get_config_dict()
        config['envs.IsaacMixedXMLEnv.num_envs'] = num_envs
        config['envs.IsaacMixedXMLEnv.spacing'] = (0., 0.025, 1.)
        if record:
            config['envs.IsaacMixedXMLEnv.create_eval_sensors'] = True
        config['envs.IsaacMixedXMLEnv.test'] = True
        config['nlimb.NLIMB.xml_root'] = folder
        gin_util.apply_bindings_from_dict(config)

        alg = gin.query_parameter('rl.train.algorithm').configurable.wrapped(self.logdir)
        alg.load()
        pi = alg.alg.pi
        env = alg.alg.env
        env.finalize_obs_norm()
        env = TimeoutWrapper(env, alg.alg.eval_max_episode_length)
        env.init_scene()
        if record:
            env.create_viewer()
        data = rl_evaluate(env, pi, nepisodes=alg.env.num_envs, t=alg.t, record_viewer=False,
                    outdir=self.logdir, num_recording_envs=num_envs if record else 0)
        alg.close()
        return data
