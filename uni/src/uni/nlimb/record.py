import os
import argparse
import wandb
import gin
from uni.utils import gin_util
from uni.rl.util import rl_evaluate
from uni.rl.wrappers.timeout_wrapper import TimeoutWrapper
from uni.utils.rng import seed


if __name__ == '__main__':
    seed(0)
    parser = argparse.ArgumentParser('viz')
    parser.add_argument('logdir')
    parser.add_argument('--folder', type=str, required=True)
    args = parser.parse_args()
    wandb.init(mode='disabled')
    gin_util.add_pytorch_external_configurables()
    gin_util.load_config_dict(os.path.join(args.logdir, 'config.json'))

    num_envs = len(os.listdir(args.folder))
    assert num_envs > 0, f'No environments found in {args.folder}'
    print(f'Found {num_envs} environments in {args.folder}')
    
    config = gin_util.get_config_dict()
    config['envs.IsaacMixedXMLEnv.num_envs'] = num_envs
    config['envs.IsaacMixedXMLEnv.spacing'] = (0., 0.025, 1.)
    config['envs.IsaacMixedXMLEnv.create_eval_sensors'] = True
    config['envs.IsaacMixedXMLEnv.test'] = True

    config['nlimb.NLIMB.xml_root'] = args.folder
    gin_util.apply_bindings_from_dict(config)

    alg = gin.query_parameter('rl.train.algorithm').configurable.wrapped(args.logdir)
    alg.load()
    pi = alg.alg.pi
    env = alg.alg.env
    env.finalize_obs_norm()
    env = TimeoutWrapper(env, 2*alg.alg.eval_max_episode_length)
    env.init_scene()
    env.create_viewer()
    rl_evaluate(env, pi, nepisodes=alg.env.num_envs, t=alg.t, record_viewer=False,
                outdir=args.logdir, num_recording_envs=num_envs)
