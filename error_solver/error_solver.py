"""
===============================================
Error Solver (:mod:`error_solver.error_solver`)
===============================================

This module contains a class for calculating and solving error matrices
based on the total derivative.
"""

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
                raise Exception('Failed to parse expression for {}'.format(y))

            self._equations.append(eq)

    def append_equation(self, equation):
        """
        Appends a new equation to the equation list.

        Parameters:
            * equation : str
                The equation string.
        """
        try:
            eq = self._parse_expr(equation)
        except:
            raise Exception('Failed to parse expression for {}'.format(equation))

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

    def equation_variables(self):
        """Returns a set of the variables in the equation list."""
        equation_variables = set()

        for x in self.equations:
            var = [str(y) for y in x.free_symbols]
            equation_variables = equation_variables.union(var)

        return equation_variables

    def restricted_symbols(self):
        """Returns a set of the restricted symbols in the input variable list."""
        restricted_symbols = set()
        variables = self.used_variables().all

        for x in variables:
            expr = parse_expr(x)
            atoms = expr.atoms(sp.NumberSymbol, sp.I, sp.zoo)

            if atoms:
                restricted_symbols = restricted_symbols.union(atoms)

        return restricted_symbols

    def values(self):
        """Returns a dictionary of the input values."""
        return {k: self.variables[k][0] for k in self.variables.keys()}

    def errors(self):
        """Returns a dictionary of the input errors."""
        return {k: self.variables[k][1] for k in self.variables.keys()}

    def used_variables(self):
        """
        Returns a namespace with lists of variables used in the equations and
        provided in the input variable dictionary.

        Returned Namespace Properties:
            * known : list
                A list of variables with known errors.
            * unknown : list
                A list of variables with unknown errors.
            * variables : list
                A list of all variables.
        """
        equation_variables = self.equation_variables()
        errors = self.errors()
        variables = sorted(errors)

        known = [k for k in variables if errors[k]!=None and k in equation_variables]
        unknown = [k for k in variables if errors[k]==None and k in equation_variables]

        return SimpleNamespace(known = known,
                               unknown = unknown,
                               all = unknown + known)

    def unused_variables(self):
        """
        Returns a set of variables present in the input list but not present
        within any equations.
        """
        equation_variables = self.equation_variables()
        errors = self.errors()
        variables = set(errors)

        return variables.difference(equation_variables)

    def missing_variables(self):
        """
        Returns a set of variables present in the equations list but not
        include in the input variable dictionary.
        """
        variables = self.used_variables().all
        equation_variables = self.equation_variables()
        return equation_variables.difference(variables)

    def partials(self):
        """Returns a list of the partial derivatives for all equations."""
        return [{v: sp.diff(x, v) for v in map(str, x.free_symbols)}
                for x in self.equations]

    def _check_restricted_symbols(self):
        """
        Returns a namespace with the status and message for the restricted
        symbol check.
        """
        restricted_symbols = self.restricted_symbols()
        status = False if restricted_symbols else True
        s = 'Symbols {} in input variable dictionary are restricted.'
        message = s.format(restricted_symbols) if not status else ''
        return SimpleNamespace(status = status, message = message)

    def _check_missing_variables(self):
        """
        Returns a namespace with the status and message for the missing
        variable check.
        """
        missing = self.missing_variables()
        status = False if missing else True
        s = 'Equation variables {} are missing from input variable dictionary.'
        message = s.format(missing) if not status else ''
        return SimpleNamespace(status = status, message = message)

    def _check_determinant_system(self):
        """
        Returns a namespace with the status and message for the determinant
        system check.
        """
        unknown = self.used_variables().unknown
        u, e = len(unknown), len(self.equations)

        status = False if u!=e else True
        s = '{} Equations != {} Unknowns. System is indeterminant.'
        message = s.format(e, u) if not status else ''

        return SimpleNamespace(status = status, message = message)

    def _check_equation_values(self):
        """
        Returns a namespace with the status and message for the equation
        value check.
        """
        tol = 1e-2
        values = self.values()
        equation_values = [abs(float(x.subs(values).evalf())) for x in self.equations]
        status = False if max(equation_values)>tol else True

        message = ['Value for {} = {} > {}.'.format(e, v, tol)
                   for v, e in zip(equation_values, self.equations) if v>tol]
        message = '\n'.join(message) if not status else ''

        return SimpleNamespace(status = status, message = message)

    def check(self):
        """
        Returns a namespace with the status and messsage for all input error
        checks.
        """
        check_methods = ('_check_restricted_symbols',
                         '_check_missing_variables',
                         '_check_determinant_system',
                         '_check_equation_values')

        checks = [getattr(self, x)() for x in check_methods]
        statuses = [x.status for x in checks]
        messages = [x.message for x in checks if x.message!='']

        status = False if False in statuses else True
        message = '\n'.join(messages) if not status else ''

        return SimpleNamespace(status = status, message = message)

    def error_matrices(self):
        """
        Returns a namespace that includes a matrix of calculated error weights.

        Returned Namespace Properties:
            * known : np.array
                The error weight matrix for the known variables.
            * unknown : np.array
                The error weight matrix for the unknown variables.
        """
        check = self.check()

        if not check.status:
            raise Exception('{}'.format(check.message))

        partials = self.partials()
        variables = self.used_variables()
        values = self.values()

        matrix = [[float(p[v].subs(values).evalf()) if v in p.keys() else 0
                   for v in variables.all] for p in partials]

        u, k = len(variables.unknown), len(variables.known)
        matrix = np.asmatrix(matrix)
        unknown = matrix[:, :u]
        known = matrix[:, -k:]

        return SimpleNamespace(unknown = unknown,
                               known = known,
                               variables = variables)

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
        """
        d = self.error_matrices()
        errors = self.errors()
        values = self.values()

        ui = np.linalg.inv(d.unknown)
        xk = np.matrix([[errors[k]] for k in d.variables.known])

        xu = np.matmul(abs(d.known), abs(xk))
        xu = np.matmul(abs(ui), xu)

        errors = {x: float(y) for x, y in zip(d.variables.known, xk)}
        unknown = {x: float(y) for x, y in zip(d.variables.unknown, xu)}
        errors.update(unknown)

        values = {k: values[k] for k in errors.keys()}

        # Percent errors
        percent_errors = {k: abs(100*errors[k]/values[k]) if values[k]!=0 else 0
                          for k in errors.keys()}

        # Summary
        s = '{:^15}|{:^25}|{:^25}|{:^25}|{}'
        summary = [s.format('Variable', 'Value', 'Error Tolerance',
                   'Percent Error', 'Unknown')]
        summary.extend([s.format(k, values[k], errors[k], percent_errors[k], k in unknown.keys())
                        for k in errors.keys()])
        summary = '\n'.join(summary)

        return SimpleNamespace(values = values,
                               errors = errors,
                               percent_errors = percent_errors,
                               summary = summary)
