"""
===================
:mod:`error_solver`
===================
"""

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr


class ErrorSolver():
    """
    Class for creating and solving error matrices for systems of equations.

    Parameters:
        equations : list
            A list of equation strings. Example:

            .. code::

               ['A = pi * r**2',
                'V = A * h']


        values : dict
            A dictionary of variable keys with values. The keys must be
            identical to those used in the equations list.

            .. code::

               {'A' : 3.14,
                'V' : 3.14,
                'r' : 1,
                'h' : 1}


        errors : dict
            A dictionary of variable keys with error tolerance values.
            The keys must be identical to those used in the equations list.
            Example:

            .. code::

               {'r' : 0.05,
                'h' : 0.05}

        tolerance : float
            The tolerance to use for equation equality check.
    """
    def __init__(self, equations, values, errors, tolerance = 0.01):
        self.equations = equations
        self.values = values
        self.errors = errors
        self.tolerance = tolerance

    def equations():
        def fget(self):
            return self._equations
        def fset(self, value):
            self._equations = []
            for x in value:
                self.append_equation(x)
        def fdel(self):
            del self._equations
        return locals()
    equations = property(**equations())

    def append_equation(self, equation):
        """
        Appends a new equation to the equation list.

        Parameters:
            equation : str
                The equation string.
        """
        try:
            e = self._parse_expr(equation)
        except:
            raise Exception('Failed to parse expression for {}'.format(equation))

        self.equations.append(e)

    def _parse_expr(self, equation):
        """
        Parses the input equation string to a sympy expression and returns
        the result.

        Parameters:
            equation : str
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
            equation : str
                The equation string to be rearranged.
        """
        f = str(equation)
        s = f.split('=')

        if len(s) == 1:
            return f
        if len(s) == 2:
            return '({})-({})'.format(*s)
        else:
            raise Exception('{} contains multiple equal signs.'.format(equation))

    def equation_variables(self):
        """Returns a set of the variables in the equation list."""
        equation_variables = set()

        for x in self.equations:
            var = set(str(y) for y in x.free_symbols)
            equation_variables |= var

        return equation_variables

    def restricted_symbols(self):
        """Returns a set of the restricted symbols in the input variable list."""
        restricted_symbols = set()
        variables = self.used_variables()
        variables = variables['unknown'] + variables['known']

        for x in variables:
            expr = parse_expr(x)
            atoms = expr.atoms(sp.NumberSymbol, sp.I, sp.zoo)

            if atoms:
                restricted_symbols |= atoms

        return restricted_symbols

    def used_variables(self):
        """
        Returns a dictionary with lists of variables used in the equations and
        provided in the input values dictionary.

        Returned dictionary keys:
            known : list
                A list of variables with known errors.
            unknown : list
                A list of variables with unknown errors.
        """
        equation_variables = self.equation_variables()

        known = [k for k in self.values if k in self.errors and k in equation_variables]
        unknown = [k for k in self.values if k not in self.errors and k in equation_variables]

        return {'known' : known, 'unknown' : unknown}

    def unused_variables(self):
        """
        Returns a set of variables present in the input list but not present
        within any equations.
        """
        equation_variables = self.equation_variables()
        variables = set(list(self.values) + list(self.errors))
        return variables - equation_variables

    def missing_variables(self):
        """
        Returns a set of variables present in the equations list but not
        included in the input variable dictionary.
        """
        equation_variables = self.equation_variables()
        variables = self.used_variables()
        variables = set(variables['unknown'] + variables['known'])
        return equation_variables - variables

    def partials(self):
        """Returns a list of the partial derivatives for all equations."""
        return [{v: sp.diff(x, v) for v in map(str, x.free_symbols)} for x in self.equations]

    def _check_restricted_symbols(self):
        """
        Returns a dictionary with the status and message for the restricted
        symbol check.
        """
        restricted_symbols = self.restricted_symbols()
        ok = not restricted_symbols
        s = 'Symbols {} in input variable dictionary are restricted.'
        message = s.format(restricted_symbols) if not ok else ''
        return {'ok' : ok, 'message': message}

    def _check_missing_variables(self):
        """
        Returns a dictionary status and message for the missing variable check.
        """
        missing = self.missing_variables()
        ok = not missing
        s = 'Equation variables {} are missing from input variable dictionary.'
        message = s.format(missing) if not ok else ''
        return {'ok' : ok, 'message' : message}

    def _check_determinant_system(self):
        """
        Returns a dictionary with the status and message for the determinant
        system check.
        """
        unknown = self.used_variables()['unknown']
        u, e = len(unknown), len(self.equations)

        ok = (u == e)
        s = '{} Equations != {} Unknowns. System is indeterminant.'
        message = s.format(e, u) if not ok else ''

        return {'ok' : ok, 'message' : message}

    def _check_equation_values(self):
        """
        Returns a dictionary with the status and message for the equation
        value check.
        """
        tol = self.tolerance
        equation_values = [abs(float(x.subs(self.values).evalf())) for x in self.equations]
        ok = (max(equation_values) <= tol)

        if ok:
            message = ''
        else:
            message = ['Value for {} = {} > {}.'.format(e, v, tol)
                       for v, e in zip(equation_values, self.equations) if v > tol]
            message = '\n'.join(message)

        return {'ok' : ok, 'message' : message}

    def check(self):
        """
        Returns a dicionary with the status and message for all input error
        checks.
        """
        check_methods = ('_check_restricted_symbols',
                         '_check_missing_variables',
                         '_check_determinant_system',
                         '_check_equation_values')

        checks = [getattr(self, x)() for x in check_methods]
        ok = (False not in set(x['ok'] for x in checks))
        if ok:
            message = ''
        else:
            message = [x['message'] for x in checks if x['message'] != '']
            message = '\n'.join(message)

        return {'ok' : ok, 'message' : message}

    def error_matrices(self):
        """
        Returns a dictionary that includes a matrix of calculated error weights.

        Returned dictionary keys:
            known : array
                The error weight matrix for the known variables.
            unknown : array
                The error weight matrix for the unknown variables.
            variables : list
                A list of all variable names.
        """
        check = self.check()

        if not check['ok']:
            raise Exception('{}'.format(check['message']))

        partials = self.partials()
        variables = self.used_variables()
        all_variables = variables['unknown'] + variables['known']

        matrix = [[float(p[v].subs(self.values).evalf()) if v in p else 0
                   for v in all_variables] for p in partials]

        u, k = len(variables['unknown']), len(variables['known'])
        matrix = np.asmatrix(matrix)
        unknown = matrix[:, :u]
        known = matrix[:, -k:]

        return {'unknown' : unknown, 'known' : known, 'variables' : variables}

    def solve(self):
        """
        Solves the error matrix and returns a dictionary with the result.

        Returned dictionary keys:
            errors : dictionary
                A dictionary of all variable names with error values.
            percent_errors : dictionary
                A dictionary of all variable names with percent errors.
            values : dictionary
                A dictionary of all variable names with values.
            summary : str
                A string summarizing the results.
        """
        d = self.error_matrices()
        ui = np.linalg.inv(d['unknown'])
        xk = np.matrix([[self.errors[k]] for k in d['variables']['known']])
        xu = np.abs(ui) @ np.abs(d['known']) @ np.abs(xk)

        errors = {x: float(y) for x, y in zip(d['variables']['known'], xk)}
        errors.update({x: float(y) for x, y in zip(d['variables']['unknown'], xu)})
        values = {k: self.values[k] for k in errors}
        pct_errors = {k: abs(100*errors[k]/self.values[k]) if self.values[k] != 0 else -1 for k in errors}

        # Summary
        v = {k: '{:.4g}'.format(values[k]) for k in errors}
        e = {k: '{:.4g}'.format(errors[k]) for k in errors}
        pe = {k: '{:.2f}'.format(pct_errors[k]) for k in errors}
        n = max(8, max(len(k) for k in errors)) + 2
        m = max(5, max(len(v[k]) for k in errors)) + 2
        o = max(15, max(len(e[k]) for k in errors)) + 2
        p = max(13, max(len(pe[k]) for k in errors)) + 2
        s = '{:^' + str(n) + '}|{:^' + str(m) + '}|{:^' + str(o) + '}|{:^' + str(p) + '}|{:^9}'

        summary = [s.format('Variable', 'Value', 'Error Tolerance', 'Percent Error', 'Unknown')]
        summary += [s.format(k, v[k], e[k], pe[k], 'True' if k in d['variables']['unknown'] else 'False') for k in errors]
        summary = '\n'.join(summary)

        return {'values' : values, 'errors' : errors, 'percent_errors' : pct_errors, 'summary' : summary}
