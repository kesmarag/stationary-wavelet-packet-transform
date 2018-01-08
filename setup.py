from setuptools import setup

setup(name='kesmarag-swpt',
      version='0.1.1',
      description='Stationary Wavelet Packet Transform',
      author='Costas Smaragdakis',
      author_email='kesmarag@gmail.com',
      url='https://github.com/kesmarag/stationary-wavelet-packet-transform',
      packages=['kesmarag.swpt'],
      package_dir={'kesmarag.swpt': './'},
      install_requires=['PyWavelets>=0.5.2'], )