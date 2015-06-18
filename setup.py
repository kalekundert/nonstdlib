import distutils.core

# Uploading to PyPI
# =================
# $ python setup.py register -r pypi
# $ python setup.py sdist upload -r pypi

version = '1.0'
distutils.core.setup(
        name='nonstdlib',
        version=version,
        author='Kale Kundert',
        url='https://github.com/kalekundert/nonstdlib',
        download_url='https://github.com/kalekundert/nonstdlib/tarball/'+version,
        license='MIT',
        description="A collection of general-purpose utilities.",
        long_description=open('README.rst').read(),
        keywords=['utilities', 'library'],
        packages=['nonstdlib'],
)
