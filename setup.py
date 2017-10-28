# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='scene_generator',
    version='0.0.1',
    description='SSDAE Scene Generator',
    author='Dimitri Henkel',
    author_email='Dimitri.Henkel@gmail.com',
    packages=find_packages(exclude=('test', 'doc'))
)