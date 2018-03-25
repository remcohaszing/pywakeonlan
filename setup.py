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
    project_urls={
        'Documentation': 'http://pywakeonlan.readthedocs.io',
        'GitHub': 'https://github.com/remcohaszing/pywakeonlan',
    },
    author='Remco Haszing',
    author_email='remcohaszing@gmail.com',
    py_modules=['wakeonlan'],
    license='MIT',
    long_description=readme,
    use_scm_version=True,
    setup_requires=['setuptools-scm ~= 1.15.7'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Networking',
    ],
    entry_points={
        'console_scripts': ['wakeonlan = wakeonlan:main'],
    })
