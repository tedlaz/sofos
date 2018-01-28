import os
import re
import sys
from setuptools import setup


if sys.hexversion < 0x3040000:
    msg = "Python version %s is unsupported, >= 3.4.0 is needed"
    print(msg % (".".join(map(str, sys.version_info[:3]))))
    exit(1)


with open("requirements.txt", "rt") as f:
    requirements = f.read().splitlines()


with open("README.md", "rt") as f:
    readme = f.read()


setup(name='sofos',
      version='0.2',
      description='Create Easily Gui Database Applications',
      long_description=readme,
      url='https://github.com/tedlaz/sofos',
      keywords=["database", "gui", "pyqt5"],
      author='Ted Lazaros',
      author_email='tedlaz@gmail.com',
      install_requires=requirements,
      license='GPLv3',
      packages=['sofos'],
      scripts=['sofos/bin/sofos_project'],
      package_data={'sofos': ['templates/images/*.png', 'templates/*.*']},
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Environment :: Console",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3 :: Only",
                   "Programming Language :: Python :: 3.6",
                   "Topic :: Utilities"]
      )
