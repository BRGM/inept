from setuptools import setup, find_packages

import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


with open('LICENSE') as f:
    license = f.read()


setup(
    name='inept',
    version=get_version('inept/__init__.py'),
    description='INteractivE oPTion system',
    author='Farid Smai',
    author_email='f.smai@brgm.fr',
    url='https://gitlab.inria.fr/charms/inept',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'click',
    ],
    setup_requires=['wheel'],
)
