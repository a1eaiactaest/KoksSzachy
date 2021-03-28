#!/usr/bin/env python3

import os 
from setuptools import setup, find_packages

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()


setup(name='KoksSzachy',
      version='0.6.7',
      description='Lubisz grać w szachy? Podobał ci się chess.com lub lichess? W takim razie pokochasz KoksSzachy! heart',
      author='a1eaiactaest, czajaproggramer, AeroRocket, igoy1, Kajtek-creator',
      license='MIT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['koksszachy'],
      classifires=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
      ],
      url="https://github.com/a1eaiactaest/KoksSzachy",
      install_requires=['chess', 'Flask'],
      python_requires='>=3.6',
      entry_points={
        "console_scripts":[
          "koksszachy=koksszachy.__main__:main",
        ]
      },
      include_package_data=True)
