#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=['tests.*', 'tests']),
    use_scm_version={
        'write_to': 'gitool/version.py'
    },
    entry_points={
        'console_scripts': ['gitool = gitool.gitool:main']
    },
)
