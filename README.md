# Error Solver

[![Build Status](https://travis-ci.com/line-mind/error_solver.svg?branch=master)](https://travis-ci.com/line-mind/error_solver)
[![Documentation Status](https://readthedocs.org/projects/error-solver/badge/?version=latest)](https://error-solver.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/line-mind/error_solver/branch/master/graph/badge.svg)](https://codecov.io/gh/line-mind/error_solver)

<!--
## Table of Contents

* [Error Solver](error_solver.rst)
-->

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

<!--
## Example: Error in Cylinder

The below example determines the propagation error tolerances for the cross
sectional area `A` and volume `V` of a cylinder given the
measurement tolerance for the radius `r` and height `h`.

```eval_rst
.. literalinclude:: ../examples/error_solver_ex1.py
```
-->
