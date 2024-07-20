from setuptools import setup, find_packages

setup(
    name='uni',
    version='0.0.1',
    author='alfie',
    description='transformer-based controller',
    package_dir={'': 'src'},
    install_requires=[
        'gin-config',
        'wandb',
        'plotly',
        'opencv-python==4.5.5.64',
        'imageio',
        'imageio-ffmpeg',
        'pydot',
        'mup',
        'pytorch3d',
        'gym',
    ]
)