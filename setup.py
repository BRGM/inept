from setuptools import setup, find_packages


setup(
    name='inept',
    use_scm_version={'write_to': 'inept/_version.py'},
    setup_requires=['setuptools_scm', 'wheel'],
    description='INteractive Editable oPTions',
    author='Farid Smai',
    author_email='f.smai@brgm.fr',
    url='https://github.com/brgm/inept',
    license='GNU GPLv3',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'click',
    ],
    python_requires='>=3.6',
)
