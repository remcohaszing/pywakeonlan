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
    description='A small python module for wake on lan.',
    url='https://github.com/remcohaszing/pywakeonlan',
    author='Remco Haszing',
    author_email='remcohaszing@gmail.com',
    py_modules=['wakeonlan'],
    license='MIT',
    long_description=readme,
    use_scm_version=True,
    setup_requires=['setuptools-scm ~= 1.15.7'],
    entry_points={
        'console_scripts': ['wakeonlan = wakeonlan:main'],
    })
