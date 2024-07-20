from uni import UniSimulator
import os
import shutil
import wandb
import gin
from uni.utils import gin_util
from uni.utils import rng
import os
import json
from subprocess import call
import glob

import torch
import numpy as np
import wandb
from uni.utils import misc


def rl_evaluate(env, pi, nepisodes, t, outdir=None, num_recording_envs=0, record_viewer=True,
                log_to_wandb=False):
    """Record episode stats."""

    if nepisodes == 0:
        return

    if log_to_wandb:
        wandb.define_metric("eval/*", step_metric="train/step")

    misc.set_env_to_eval_mode(env)
    pi.eval()

    obs = env.reset()

    asset_files = sorted([os.path.basename(f) for f in
                                    glob.glob(os.path.join(env.asset_root, '*.xml'))])

    # record
    if record_viewer:
        env.record_viewer(os.path.join(outdir, 'viewer.mp4'))
    num_recording_envs = min(num_recording_envs, env.num_envs)
    for i in range(num_recording_envs):
        env.record_env(i, os.path.join(outdir, f'env{i}.mp4'))

    obs = env.reset()
    batch_dones = torch.ones(env.num_envs, device=env.device, dtype=torch.bool)
    batch_length = torch.zeros(env.num_envs, device=env.device, dtype=torch.float)
    batch_reward = torch.zeros(env.num_envs, device=env.device, dtype=torch.float)
    
    # 获取 link 索引
    gym = env.gym
    sim = env.sim
    robot_handle = env.robots[0]  # 假设只有一个机器人
    asset = gym.get_actor_asset(sim, robot_handle)
    link_name = "body"  # 指定 link 名称
    link_index = None
    num_links = gym.get_asset_rigid_body_count(asset)
    for i in range(num_links):
        if gym.get_asset_rigid_body_name(asset, i) == link_name:
            link_index = i
            break

    if link_index is None:
        raise ValueError(f"Link named {link_name} not found")

    # 准备记录质心位置
    com_positions = []


    while torch.any(batch_dones):
        with torch.no_grad():
            ac = pi(obs).action
            obs, rews, dones, _ = env.step(ac)
        assert dones.shape == batch_dones.shape
        batch_length[batch_dones] += 1
        batch_reward[batch_dones] += rews[batch_dones]
        torch.logical_and(torch.logical_not(dones), batch_dones, out=batch_dones)
        # 记录当前状态下的 link 质心位置

        rigid_body_states = gym.get_actor_rigid_body_states(env, robot_handle, gymapi.STATE_ALL)
        link_state = rigid_body_states[link_index]
        com_position = link_state.pose.p
        com_position_np = np.array([com_position.x, com_position.y, com_position.z])
        com_positions.append(com_position_np.tolist())  # 将 numpy 数组转换为列表以便于序列化



    episode_lengths = batch_length.cpu().numpy().tolist()
    episode_rewards = batch_reward.cpu().numpy().tolist()

    episode_lengths_map = {}
    episode_rewards_map = {}
    mean_length = {}
    mean_reward = {}
    median_length = {}
    median_reward = {}
    for i, name in enumerate(asset_files):
        episode_lengths_map[name] = episode_lengths[i::len(asset_files)]
        episode_rewards_map[name] = episode_rewards[i::len(asset_files)]
        mean_length[name] = float(np.mean(episode_lengths_map[name]))
        mean_reward[name] = float(np.mean(episode_rewards_map[name]))
        median_length[name] = float(np.median(episode_lengths_map[name]))
        median_reward[name] = float(np.median(episode_rewards_map[name]))

    data = {
        'episode_lengths': episode_lengths_map,
        'episode_rewards': episode_rewards_map,
        'mean_length': mean_length,
        'mean_reward': mean_reward,
        'median_length': median_length,
        'median_reward': median_reward,
        'com_positions': com_positions
    }

    print(data)

    if outdir is not None:
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, 'data.txt'), 'w') as f:
            json.dump(data, f)

    if log_to_wandb:
        wandb.log({'eval/mean_episode_rewards': data['mean_reward'],
                   'eval/mean_episode_lengths': data['mean_length'],
                   'eval/median_episode_rewards': data['median_reward'],
                   'eval/median_episode_lengths': data['median_length'],
                   'train/step': t})

    # write videos
    if record_viewer:
        outfile = os.path.join(outdir, 'viewer.mp4')
        env.write_viewer_video()
        if log_to_wandb:
            wandb.log({'eval/viewer': wandb.Video(outfile), 'train/step': t})

    fnames = []
    for i in range(num_recording_envs):
        outfile = os.path.join(outdir, f'env{i}.mp4')
        env.write_env_video(i)
        fnames.append(outfile)

    if num_recording_envs > 0:
        outfile = os.path.join(outdir, 'all_envs.mp4')
        merge_cmd = ['ffmpeg']
        for fname in fnames:
            merge_cmd += ['-i', fname]
        merge_cmd += ['-filter_complex', 'hstack', outfile]
        call(merge_cmd)
        if log_to_wandb:
            wandb.log({'eval/envs': wandb.Video(outfile), 'train/step': t})

    env.reset()
    misc.set_env_to_train_mode(env)
    pi.train()
    return data

from uni.rl.wrappers.timeout_wrapper import TimeoutWrapper
import matplotlib.pyplot as plt
import time

class MyUNI(UniSimulator):
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


if __name__ == '__main__':
    uni = MyUNI('mjcf_model/tests/test8','/home/ps/pan1/files/Sam/grammar_mjcf-master/my_config/grammar.gin')
    uni.simulate(40000000)
    uni.close()
    # UniSimulator.visual('mjcf_model/tests/test8','/home/ps/pan1/files/Sam/grammar_mjcf-master/my_config/grammar.gin')
    # UniSimulator.terrain_visual('/home/ps/pan1/files/Sam/grammar_mjcf-master/mjcf_model/2024-04-25_10-23-29', mode='test')