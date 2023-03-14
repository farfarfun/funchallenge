import sys
from os import path

from setuptools import find_packages, setup

import time


install_requires = ['sqlalchemy','darksecret']

setup(name='darkchallenge',
      version=time.strftime("%Y%m%d%H%M", time.localtime()),
      description='darkchallenge',
      author='niuliangtao',
      author_email='1007530194@qq.com',
      url='https://github.com/1007530194',
      packages=find_packages(),
      package_data={"": ["*.js", "*.*"]},
      install_requires=install_requires,
      )
