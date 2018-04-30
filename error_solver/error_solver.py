"""
===============================================
Error Solver (:mod:`error_solver.error_solver`)
===============================================

This module contains a class for calculating and solving error matrices.
"""

import sys
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from types import SimpleNamespace


class ErrorSolver():
    """
    Error solver class.
    """
    def __init__(self, equations, variables):
        self.variables = variables
        self.equations = equations

    @property
    def equations(self):
        return self._equations

    @equations.setter
    def equations(self, x):
        self._equations = [self._parse_expr(y) for y in x]

    def append(self, equation):
        """
        Appends a new equation to the equation list.

        Parameters:
            * equation : str
                The equation string.
        """
        eq = self._parse_expr(equation)
        self.equations.append(eq)

    def _parse_expr(self, equation):
        """
        Parses the input equation string to a sympy expression and returns
        the result.

        Parameters:
            * equation : str
                The equation string to be parsed.
        """
        s = self._set_equal_to_zero(equation)
        return parse_expr(s)

    def _set_equal_to_zero(self, equation):
        """
        If the input equation string contains an equal sign, rearranges
        the string so that equation is equal to zero to be compatible
        with sympy.

        Parameters:
            * equation : str
                The equation string to be rearranged.
        """
        f = str(equation)
        s = f.split('=')

        if len(s)==1:
            return f
        if len(s)==2:
            return '({})-({})'.format(*s)
        else:
            raise Exception('Error:: {} contains multiple equal signs.'.format(equation))

    def variable_summary(self):
        """
        Returns a namespace with various variable properties.

        Namespace Properties:
            * values : dictionary
                A dictionary of variable names and input values.
            * errors : dictionary
                A dictionary of variable names and input error values.
            * known : list
                A list of variable names that have known input error values.
            * unknown : list
                A list of variable names for which error values are unknown.
            * variables : list
                A list of all input variable names.
            * equations : list
                A list of all parsed input equations.
            * partials : list of dictionaries
                A list of dictionaries with the variable names and partial
                derivatives.
        """
        var = SimpleNamespace()
        eq_vars = []

        for x in self.equations:
            eq_vars.extend([str(y) for y in x.free_symbols])

        eq_vars = set(eq_vars)

        var.values = {k: self.variables[k][0] for k in self.variables.keys()}
        var.errors = {k: self.variables[k][1] for k in self.variables.keys()}

        variables = sorted(var.errors)
        var.known = [k for k in variables if var.errors[k]!=None and k in eq_vars]
        var.unknown = [k for k in variables if var.errors[k]==None and k in eq_vars]
        var.variables = var.unknown + var.known

        var.equations = self.equations
        var.partials = [{v: sp.diff(x, v) for v in map(str, x.free_symbols)}
                        for x in self.equations]

        # Check that number of equations equals number of unknowns
        n, m = len(var.unknown), len(var.equations)
        if n!=m:
            raise Exception('Error:: {} Equations != {} Unknowns. Number of ' \
                            'equations must match number of unknowns.'.format(m, n))

        # Check that there are no missing variables
        s = eq_vars.difference(var.variables)
        if len(s)!=0:
            raise Exception('Error:: Equation variables {} are missing from ' \
                            'input variable dictionary.'.format(s))
        return var

    def error_matrix(self):
        """
        Returns a namespace that includes a matrix of calculated error weights.

        Namespace Properties:
            * matrix : np.array
                The calculated error matrix
            * All properties included with variable_summary method.
        """
        var = self.variable_summary()

        matrix = [[float(p[v].subs(var.values).evalf()) if v in p.keys() else 0
                   for v in var.variables] for p in var.partials]

        var.matrix = np.asmatrix(matrix)
        return var

    def solve(self):
        """
        Solves the error matrix and returns a namespace with the result.

        Namespace Properties:
            * known_errors : dictionary
                A dictionary of the known input error values.
            * unknown_errors : dictionary
                A dictionary of the solved unknown error values.
            * known_matrix : np.array
                The error weight matrix for the known variables.
            * unknown_matrix : np.array
                The error weight matrix for the unknown variables.
            * errors : dictionary
                A dictionary of all variable names with error values.
            * percent_errors : dictionary
                A dictionary of all variable names with percent errors.
            * All properties included with variable_summary method.
        """
        var = self.error_matrix()
        n, m = len(var.unknown), len(var.known)

        k1 = var.matrix[:n, :n] # Unknown error matrix
        k2 = var.matrix[:n:, -m:] # Known error matrix

        known_errors = [var.errors[k] for k in var.known]

        c = -np.matmul(k2, known_errors) # Augmented matrix
        i = np.linalg.inv(k1) # Inverse unknown error matrix
        unknown_errors = np.matmul(i, c.T)

        # Summarize results
        var.unknown_matrix = k1
        var.known_matrix = k2

        var.known_errors = {x: float(y) for x, y in zip(var.known, known_errors)}
        var.unknown_errors = {x: float(y) for x, y in zip(var.unknown, unknown_errors)}
        var.errors = {**var.unknown_errors, **var.known_errors}

        # Percent errors
        var.percent_errors = {}

        for k in var.errors.keys():
            value = var.values[k]

            if value==0:
                value = sys.float_info.min

            var.percent_errors[k] = abs(100*var.errors[k]/value)

        return var
