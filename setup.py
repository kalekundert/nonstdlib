#!/usr/bin/env python
# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re
with open('nonstdlib/__init__.py') as file:
    version_pattern = re.compile("__version__ = '(.*)'")
    version = version_pattern.search(file.read()).group(1)

with open('README.rst') as file:
    readme = file.read()

setup(
    name='nonstdlib',
    version=version,
    author='Kale Kundert',
    author_email='kale@thekunderts.net',
    description='A collection of general-purpose utilities',
    long_description=readme,
    url='https://github.com/kalekundert/nonstdlib',
    packages=[
        'nonstdlib',
    ],
    include_package_data=True,
    install_requires=[
        'six',
    ],
    license='MIT',
    zip_safe=False,
    keywords=[
        'nonstdlib',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
)
