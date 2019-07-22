import setuptools
import os.path

with open('README.md', 'r') as fh:
    long_description = fh.read()

version_file = open(os.path.join('hydrate', 'VERSION'))
version = version_file.read().strip()

setuptools.setup(
    name='hydrate',
    version=version,
    author='andrewDoing',
    author_email='andrew.doing@mst.edu',
    description='A package to generate an HLD for your kubernetes cluster',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/andrewDoing/hydrate',
    install_requires=['kubernetes', 'ruamel.yaml'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=['hydrate'],
    entry_points={
          'console_scripts': [
              'hydrate = hydrate.__main__:main'
          ]
    },
)
