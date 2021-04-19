#!/usr/bin/env python3

from setuptools import find_packages, setup

import os
directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

description = 'Lubisz grać w szachy? Podobał ci się chess.com lub lichess? W takim razie pokochasz KoksSzachy! <3'

setup(name='KoksSzachy',
      version='0.8.17',
      description=description,
      author='a1eaiactaest,czajaproggramer,AeroRocket,igoy1,Kajtek-creator',
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
      python_requires='>=3.7',
      entry_points={
        "console_scripts":[
          "koksszachy=koksszachy.play:main", 
        ]
      },
      include_package_data=True)
