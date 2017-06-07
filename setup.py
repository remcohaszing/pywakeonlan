#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Install the wakeonlan module.

"""
from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

setup(
    name='wakeonlan',
    version='0.2.2',
    description='A small python module for wake on lan.',
    url='https://github.com/remcohaszing/pywakeonlan',
    author='Remco Haszing',
    author_email='remcohaszing@gmail.com',
    py_modules=['wakeonlan'],
    license='WTFPL',
    long_description=readme,
    entry_points={
        'console_scripts': ['wol = wakeonlan:main']
    })
