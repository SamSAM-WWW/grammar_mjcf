"""Joint optimization of design and control."""

from typing import Type
import inspect
import gin
import wandb
from uni.rl import Algorithm
from uni.utils import subproc_worker
from uni.envs import IsaacMixedXMLEnv
from uni.utils.misc import ActionBounds
from uni.utils import gin_util


# Due to a memory leak in IsaacGym, the environment must be run in a subprocess.
def subproc_env(env_cls):
    config = gin_util.get_config_dict()

    class GinWrapper(env_cls):
        def __init__(self, *args, **kwargs):
            import uni.nlimb
            import uni.tasks
            import uni.envs
            import uni.utils
            import uni.rl
            gin_util.add_pytorch_external_configurables()
            gin_util.apply_bindings_from_dict(config)
            env_cls.__init__(self, *args, **kwargs)

    subproc_cls = subproc_worker(GinWrapper, ctx='spawn', daemon=True)

    class SubprocIsaacEnv():
        def __init__(self, *args, **kwargs):
            self.env = None
            self._args = args
            self._kwargs = kwargs
            self._create_env()
            self.num_envs = self.env.get_num_envs().results
            self.device = self.env.get_device().results
            self.observation_space = self.env.get_observation_space().results
            self.action_space = self.env.get_action_space().results
            self.asset_root = self.env.get_asset_root().results
            self.action_bounds = ActionBounds(self.action_space, self.device)

        def _create_env(self, test=False):
            if self.env is not None:
                self.env.close()
            self.env = subproc_cls(*self._args, **self._kwargs, test=test)

        def init_scene(self, test=False):
            self._create_env(test)

        def close(self):
            if self.env is not None:
                self.env.close()
                self.env = None

    def _add_command(name):
        def remote_fn(self, *args, **kwargs):
            return getattr(self.env, name)(*args, **kwargs).results
        setattr(SubprocIsaacEnv, name, remote_fn)

    for name, _ in inspect.getmembers(subproc_cls, inspect.isfunction):
        if name[0] == '_' or name in ['init_scene', 'close']:
            continue
        _add_command(name)

    return SubprocIsaacEnv


@gin.configurable(module='nlimb')
class NLIMB(Algorithm):
    def __init__(self,
                 logdir,
                 env: Type[IsaacMixedXMLEnv],
                 rl_algorithm: Type[Algorithm],
                 xml_root: str = 'xmls',
                 ):

        Algorithm.__init__(self, logdir)
        env = subproc_env(env)(asset_root=xml_root)
        self.env = env
        self.alg = rl_algorithm(logdir, env=self.env)
        self.t = 0
        wandb.define_metric('nlimb/*', step_metric='train/step')

    def step(self):
        self.t = self.alg.step()
        return self.t

    def evaluate(self):
        data = self.alg.evaluate()
        return data

    def save(self):
        self.alg.save()

    def load(self, t=None):
        self.t = self.alg.load(t)
        return self.t

    def close(self):
        self.env.close()
        self.alg.close()
