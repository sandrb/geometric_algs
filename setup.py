#!/usr/bin/env python3.6
"""
Setup file to setup the project.

"""
from setuptools import find_packages
from setuptools import setup

from spanners import __version__

with open('README.rst') as file:
    readme = file.read()

setup(
    name='spanners',
    version=__version__,
    description='Calculate geometric spanners amidst obstacles.',
    long_description=readme,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Topic :: Education :: Testing',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='spanners polygon obstacle',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        # Cheese shop dependencies
        'docopt ~= 0.6.2',
        'matplotlib ~= 1.5.3',
        'pyvisgraph ~= 0.1.4',
    ],
    entry_points={
        'console_scripts': [
            'spanners = spanners.cli:main',
        ]
    },
    test_suite='tests',
    zip_safe=False,
)
