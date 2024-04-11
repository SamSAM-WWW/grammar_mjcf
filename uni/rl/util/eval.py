"""Evaluation for RL Environments."""
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
    while torch.any(batch_dones):
        with torch.no_grad():
            ac = pi(obs).action
            obs, rews, dones, _ = env.step(ac)
        assert dones.shape == batch_dones.shape
        batch_length[batch_dones] += 1
        batch_reward[batch_dones] += rews[batch_dones]
        torch.logical_and(torch.logical_not(dones), batch_dones, out=batch_dones)

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
