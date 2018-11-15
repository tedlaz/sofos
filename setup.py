import os
import re
import sys

from setuptools import setup

requires = [
        'PyQt5',
        'PyYAML',
        ]

setup(name='sofos',
        version='0.9.6',
        description='GUI Database Applications Generator',
        long_description='Create GUI Database Applications fast',
        url='https://github.com/tedlaz/sofos',
        keywords=["database", "GUI", "pyqt5"],
        author='Ted Lazaros',
        author_email='tedlaz@gmail.com',
        install_requires=requires,
        license='GPLv3',
        packages=['sofos'],
        scripts=['sofos/bin/sofos-project'],
        python_requires=">=3.4.0",
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
