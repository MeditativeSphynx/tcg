from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='TCG',
    url='https://github.com/MeditativeSphynx/tcg',
    version='alpha-1.0',
    description='A desktop application that interacts with different '\
        'APIs and databases',
    long_description=long_description
)