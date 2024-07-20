"""Basic training loop."""
import os
import time
import gin
from uni.utils import rng, gin_util


class Algorithm(object):
    """Interface for Deep Learning algorithms."""

    def __init__(self, logdir):
        """Init."""
        self.logdir = logdir

    def step(self):
        """Step the optimization.

        This function should return the step count of the algorithm.
        """
        raise NotImplementedError

    def evaluate(self):
        """Evaluate model."""
        raise NotImplementedError

    def save(self):
        """Save model."""
        raise NotImplementedError

    def load(self, t=None):
        """Load model.

        This function should return the step count of the algorithm.
        """
        raise NotImplementedError

    def close(self):
        """Clean up at end of training."""
        pass


@gin.configurable(module='rl')
def train(logdir,
          algorithm,
          seed=0,
          eval=False,
          eval_period=None,
          save_period=None,
          maxt=None,
          maxseconds=None,
          make_logdir_unique=False):
    """Basic training loop.

    Args:
        logdir (str):
            The base directory for the training run.
        algorithm_class (Algorithm):
            The algorithm class to use for training. A new instance of the class
            will be constructed.
        seed (int):
            The initial seed of this experiment.
        eval (bool):
            Whether or not to evaluate the model throughout training.
        eval_period (int):
            The period with which the model is evaluated.
        save_period (int):
            The period with which the model is saved.
        maxt (int):
            The maximum number of timesteps to train the model.
        maxseconds (float):
            The maximum amount of time to train the model.
        make_logdir_unique (bool):
            If True, ensures that the logdir is unique to avoid name collisions.
    """
    if make_logdir_unique:
        logdir += f'_{time.time_ns()}'
    os.makedirs(logdir, exist_ok=True)
    rng.seed(seed)
    alg = algorithm(logdir=logdir)
    config = gin.operative_config_str()
    print("=================== CONFIG ===================")
    print(config)
    with open(os.path.join(logdir, 'config.gin'), 'w') as f:
        f.write(config)
    gin_util.save_config_dict(os.path.join(logdir, 'config.json'))
    time_start = time.monotonic()
    t = alg.load()
    if save_period:
        last_save = (t // save_period) * save_period
    if eval_period:
        last_eval = (t // eval_period) * eval_period
    with open('log.txt', 'a+') as f:
        f.write(f'start: {time.asctime(time.localtime(time.time()))}\n')
        try:
            while True:
                if maxt and t >= maxt:
                    break
                if maxseconds and time.monotonic() - time_start >= maxseconds:
                    break
                t = alg.step()
                if save_period and (t - last_save) >= save_period:
                    f.write(f'end: {time.asctime(time.localtime(time.time()))}\n')
                    data = alg.evaluate()
                    f.write(f'eval: {time.asctime(time.localtime(time.time()))}\n')
                    f.write(f'{data}\n')
                    break
                    # alg.save()
                    # last_save = t
                if eval and (t - last_eval) >= eval_period:
                    data = alg.evaluate()
                    print(data)
                    last_eval = t
        except KeyboardInterrupt:
            print("Caught Ctrl-C. Saving model and exiting...")
    alg.save()
    alg.close()
    
