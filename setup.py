import os
import re
import sys
from setuptools import setup


if sys.hexversion < 0x3040000:
    msg = "Python version %s is unsupported, >= 3.4.0 is needed"
    print(msg % (".".join(map(str, sys.version_info[:3]))))
    exit(1)


setup(name='sofos',
      version='0.9.6',
      description='Gui Database Applications Generator',
      long_description='Create Gui Database Applications fast',
      url='https://github.com/tedlaz/sofos',
      keywords=["database", "gui", "pyqt5"],
      author='Ted Lazaros',
      author_email='tedlaz@gmail.com',
      install_requires=['PyQt5', 'PyYAML'],
      license='GPLv3',
      packages=['sofos'],
      scripts=['sofos/bin/sofos-project'],
      package_data={'sofos': ['models/*.py',
                              'qt/*.py',
                              'templates/images/*.png',
                              'templates/*.*',
                              'templates/zforms/*.py']},
      classifiers=["Development Status :: 4 - Beta",
                   "Environment :: Console",
                   "Environment :: X11 Applications :: Qt",
                   "Environment :: Win32 (MS Windows)",
                   "Intended Audience :: Developers",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3 :: Only",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Topic :: Software Development :: Build Tools"]
      )
