import os
from glob import glob
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name = 'error_solver',
      version = '0.0.0',
      author = 'Matt Pewsey',
      description = 'Estimates error tolerances for systems of equations based on the total derivatives',
      long_description = long_description,
      url = 'https://github.com/line-mind/error_solver',
      license = 'BSD 3-Clause License',
      packages = find_packages(),
      include_package_data = True,
      scripts = [],
      install_requires = ['numpy', 'sympy'],
      dependency_links = [],
      keywords = ['error-estimation', 'measurement-tolerances', 'error-tolerances'],
      classifiers = ['Programming Language :: Python :: 3',
                     'Operating System :: OS Independent',
                     'License :: OSI Approved :: BSD License'],
      python_requires = '>=3.5')
