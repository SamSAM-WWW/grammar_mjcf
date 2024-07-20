import sys
import os
import argparse
import time
import random
import pickle
import csv
import ast
import numpy as np
from copy import deepcopy
import torch
from torch import optim
import torch.nn.functional as F

def search_algo(args):
    # iniailize random seed
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.set_num_threads(1)


if __name__ == '__main__':
    torch.set_default_dtype(torch.float64)
    args_list = ['--task', 'FlatTerrainTask',
                 '--grammar-file', '../../data/designs/grammar_apr30.dot',
                 '--num-iterations', '2000',
                 '--mpc-num-processes', '32',
                 '--lr', '1e-4',
                 '--eps-start', '1.0',
                 '--eps-end', '0.1',
                 '--eps-decay', '0.3',
                 '--eps-schedule', 'exp-decay',
                 '--eps-sample-start', '1.0',
                 '--eps-sample-end', '0.1',
                 '--eps-sample-decay', '0.3',
                 '--eps-sample-schedule', 'exp-decay',
                 '--num-samples', '16', 
                 '--opt-iter', '25', 
                 '--batch-size', '32',
                 '--states-pool-capacity', '10000000',
                 '--depth', '40',
                 '--max-nodes', '80',
                 '--save-dir', './trained_models/',
                 '--log-interval', '100',
                 '--eval-interval', '1000',
                 '--max-trials', '1000',
                 '--num-eval', '1',
                 '--no-noise']

    solve_argv_conflict(args_list)
    parser = get_parser()
    args = parser.parse_args(args_list + sys.argv[1:])

    if not args.test:
        args.save_dir = os.path.join(args.save_dir, args.task, get_time_stamp())
        try:
            os.makedirs(args.save_dir, exist_ok = True)
        except OSError:
            pass
        
        fp = open(os.path.join(args.save_dir, 'args.txt'), 'w')
        fp.write(str(args_list + sys.argv[1:]))
        fp.close()
    search_algo(args)