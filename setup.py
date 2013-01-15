from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    with open('cacheobj/version.txt') as f:
        return f.read().strip()


def get_readme():
    try:
        with open('README.rst') as f:
            return f.read().strip()
    except IOError:
        return ''

setup(
    name='cacheobj',
    version=get_version(),
    description='An cache interface with python object-property interface.',
    long_description=get_readme(),
    author='Jeong YunWon',
    author_email='jeong+cacheobj@youknowone.org',
    url='https://github.com/youknowone/cacheobj',
    packages=(
        'cacheobj',
        'cacheobj/backends',
    ),
    package_data={
        'cacheobj': ['version.txt']
    },
    install_requires=[
        'distribute',
    ],
)