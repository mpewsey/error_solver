"""
===============================================
Error Solver (:mod:`error_solver.error_solver`)
===============================================

This module contains a class for calculating and solving error matrices
based on the total derivative.
"""

import sys
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from types import SimpleNamespace


class ErrorSolver():
    """
    Class for creating and solving error matrices for systems of equations.

    Parameters:
        * equations : list
            A list of equation strings. For example,

            .. code-block:: python

               ['A = pi * r**2',
                'V = A * h']

        * variables : dict
            A dictionary of variable keys with a list or tuple of
            (values, error_values). The variable keys must be identical to
            those used in the equations list. If the error value is an
            unknown value to be solved for, input None for the error.
            For example,

            .. code-block:: python

               {'A' : (3.14, None),
                'V' : (3.14, None),
                'r' : (1, 0.05),
                'h' : (1, 0.05)}

    """
    def __init__(self, equations, variables):
        self.variables = variables
        self.equations = equations

    @property
    def equations(self):
        return self._equations

    @equations.setter
    def equations(self, x):
        self._equations = []

        for y in x:
            try:
                eq = self._parse_expr(y)
            except:
                raise Exception('Failed parse_expr for {}'.format(y))

            self._equations.append(eq)

    def append(self, equation):
        """
        Appends a new equation to the equation list.

        Parameters:
            * equation : str
                The equation string.
        """
        try:
            eq = self._parse_expr(equation)
        except:
            raise Exception('Failed parse_expr for {}'.format(equation))

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
            raise Exception('{} contains multiple equal signs.'.format(equation))

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
        ns = SimpleNamespace()
        equation_vars = []

        for x in self.equations:
            equation_vars.extend([str(y) for y in x.free_symbols])

        equation_vars = set(equation_vars)

        ns.values = {k: self.variables[k][0] for k in self.variables.keys()}
        ns.errors = {k: self.variables[k][1] for k in self.variables.keys()}

        variables = sorted(ns.errors)
        ns.known = [k for k in variables if ns.errors[k]!=None and k in equation_vars]
        ns.unknown = [k for k in variables if ns.errors[k]==None and k in equation_vars]
        ns.variables = ns.unknown + ns.known

        ns.equations = self.equations
        ns.partials = [{v: sp.diff(x, v) for v in map(str, x.free_symbols)}
                        for x in self.equations]

        # Check that there are no missing variables
        s = equation_vars.difference(ns.variables)
        if len(s)!=0:
            raise Exception('Equation variables {} are missing from ' \
                            'input variable dictionary.'.format(s))

        # Check that number of equations equals number of unknowns
        n, m = len(ns.unknown), len(ns.equations)
        if n!=m:
            raise Exception('{} Equations != {} Unknowns. Number of ' \
                            'equations must match number of unknowns.'.format(m, n))

        return ns

    def error_matrix(self):
        """
        Returns a namespace that includes a matrix of calculated error weights.

        Namespace Properties:
            * matrix : np.array
                The calculated error matrix
            * known_matrix : np.array
                The error weight matrix for the known variables.
            * unknown_matrix : np.array
                The error weight matrix for the unknown variables.
            * All properties included with variable_summary method.
        """
        ns = self.variable_summary()

        matrix = [[abs(float(p[v].subs(ns.values).evalf())) if v in p.keys() else 0
                   for v in ns.variables] for p in ns.partials]

        ns.matrix = np.asmatrix(matrix)

        n, m = len(ns.unknown), len(ns.known)
        ns.unknown_matrix = ns.matrix[:, :n]
        ns.known_matrix = ns.matrix[:, -m:]

        return ns

    def solve(self):
        """
        Solves the error matrix and returns a namespace with the result.

        Namespace Properties:
            * errors : dictionary
                A dictionary of all variable names with error values.
            * percent_errors : dictionary
                A dictionary of all variable names with percent errors.
            * values : dictionary
                A dictionary of all variable names with values.
            * summary : str
                A string summarizing the results.
            * All properties included with error_matrix method.
        """
        ns = self.error_matrix()

        known_errors = [ns.errors[k] for k in ns.known]
        c = np.matmul(ns.known_matrix, known_errors) # Augmented matrix
        i = np.linalg.inv(ns.unknown_matrix) # Inverse unknown error matrix

        c = c.tolist()[0]
        i = i.tolist()

        unknown_errors = [sum(abs(y*z) for y, z in zip(x, c)) for x in i]

        # Summarize results
        ns.known_errors = {x: float(y) for x, y in zip(ns.known, known_errors)}
        ns.unknown_errors = {x: float(y) for x, y in zip(ns.unknown, unknown_errors)}
        ns.errors = {**ns.unknown_errors, **ns.known_errors}

        # Percent errors
        ns.percent_errors = {}

        for k in ns.errors.keys():
            value = ns.values[k]

            if value==0:
                value = sys.float_info.min

            ns.percent_errors[k] = abs(100*ns.errors[k]/value)

        summary = ['{:<10} {:<25} {:<25} {:<25}'.format('Variable', 'Value',
                   'Error Tolerance', 'Percent Error')]

        summary.extend(['{:<10} {:<25} {:<25} {:<25}'.format(k, ns.values[k],
                        ns.errors[k], ns.percent_errors[k])
                        for k in ns.errors.keys()])

        ns.summary = '\n'.join(summary)

        return ns
