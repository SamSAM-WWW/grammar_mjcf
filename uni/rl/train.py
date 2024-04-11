from uni.utils import gin_util
from uni.rl.trainer import train


@gin_util.wandb_main
def main():
    train()

if __name__ == '__main__':
    main()
