==========================
Error Solver Documentation
==========================

.. image:: https://img.shields.io/pypi/pyversions/error_solver.svg
    :target: #

.. image:: https://img.shields.io/pypi/v/error_solver.svg
    :target: #

.. image:: https://travis-ci.com/mpewsey/error_solver.svg?branch=master
    :target: https://travis-ci.com/mpewsey/error_solver

.. image:: https://readthedocs.org/projects/error-solver/badge/?version=latest
    :target: https://error-solver.readthedocs.io/en/latest/?badge=latest

.. image:: https://codecov.io/gh/mpewsey/error_solver/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mpewsey/error_solver

About
=====
This package contains classes for estimating the propagation error tolerances
for a system of equations.

Installation
============

This package may be installed via pip:

.. code-block:: none

    pip install error_solver


The above installation only install the dependencies required for the
`ErrorSolverPy` class. To also install the dependencies necessary for the
`ErrorSolver` class, use the following command instead:

.. code-block:: none

    pip install error_solver[all]


Example: Error in Cylinder
==========================
The below example determines the propagation error tolerances for the cross
sectional area `A` and volume `V` of a cylinder given the
measurement tolerance for the radius `r` and height `h`.

.. literalinclude:: ../examples/error_solver_ex1.py


API Documentation
=================
.. toctree::
    :maxdepth: 1

    solvers
    data
