#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

from romeo_sierra import __version__

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Harrison Richard Mouat & Shashwat Kansal",
    author_email='harrison.mouat19@imperial.ac.uk & shashwat.kansal19@imperial.ac.uk',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="Romeo Sierra",
    entry_points={
        'console_scripts': [
            'rs=romeo_sierra.cli:main', 'rs-bt=romeo_sierra.cli:backtest'
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='romeo_sierra',
    name='romeo_sierra',
    packages=find_packages(exclude=['docs', 'tests*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/harry212001/romeo_sierra',
    version=__version__,
    zip_safe=False,
)
