# Error Solver

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/error_solver.svg)
![PyPI](https://img.shields.io/pypi/v/error_solver.svg)
[![Build Status](https://travis-ci.com/mpewsey/error_solver.svg?branch=master)](https://travis-ci.com/mpewsey/error_solver)
[![Documentation Status](https://readthedocs.org/projects/error-solver/badge/?version=latest)](https://error-solver.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/mpewsey/error_solver/branch/master/graph/badge.svg)](https://codecov.io/gh/mpewsey/error_solver)

## About

This package contains classes for estimating the propagation error tolerances
for a system of equations.

## Installation

This package may be installed via pip:

```
pip install error_solver
```

The above installation only install the dependencies required for the
`ErrorSolverPy` class. To also install the dependencies necessary for the
`ErrorSolver` class, use the following command instead:

```
pip install error_solver[all]
```

## Example: Error in Cylinder

The below example determines the propagation error tolerances for the cross sectional
area `A` and volume `V` of a cylinder given the measurement tolerance for the radius
`r` and height `h`.

```python
from error_solver import ErrorSolver

# Define the equations
EQUATIONS = [
    'A = pi * r**2',
    'V = A * h'
]

# Solve the equations by some means and assemble the values in a dictionary
values = {
    'h': 12,
    'r': 5,
    'A': 78.54,
    'V': 942.48
}

# Define the known error tolerances
errors = {
    'h': 0.05,
    'r': 0.05
}

solver = ErrorSolver(EQUATIONS)
solver.solve(values, errors)
#           value      error  pct_error  is_calc
# var
# A     78.539816   1.570796   2.000000     True
# V    942.477796  22.776547   2.416667     True
# h     12.000000   0.050000   0.416667    False
# r      5.000000   0.050000   1.000000    False
```
