#!/usr/bin/env python3

import distutils.core
import subprocess, shlex

# Uploading to PyPI
# =================
# The first time only:
# $ python setup.py register -r pypi
#
# Every version bump:
# $ git tag <version>; git push
# $ python setup.py sdist upload -r pypi

version = '1.4'
distutils.core.setup(
        name='nonstdlib',
        version=version,
        author='Kale Kundert',
        author_email='kale@thekunderts.net',
        url='https://github.com/kalekundert/nonstdlib',
        download_url='https://github.com/kalekundert/nonstdlib/tarball/'+version,
        license='MIT',
        description="A collection of general-purpose utilities.",
        long_description=open('README.rst').read(),
        keywords=['utilities', 'library'],
        packages=['nonstdlib'],
)
