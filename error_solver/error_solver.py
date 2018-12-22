import sympy
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
from ._base_error_solver import _BaseErrorSolver

__all__ = ['ErrorSolver']


class ErrorSolver(_BaseErrorSolver):
    """
    A class for solving systems of equations for their propagation error
    tolerances based on equation strings. This method accepts equations
    defined as strings or `sympy` expressions. The required partial
    derivatives are evaluated using the equations.

    Parameters
    ----------
    equations : list
        A list of equation string or string convertible equation objects.
    tol : float
        The tolerance used for verifying that values satisfy equations.

    Examples
    --------
    .. literalinclude:: ../../examples/error_solver_ex1.py
    """
    def __init__(self, equations, tol=0.01):
        self.equations = []
        for x in equations:
            self.add_equation(x)
        self.tol = tol

    def add_equation(self, equation):
        """
        Parses the equation and adds it to the class equation list. If parsing
        fails, raises an exception.

        Parameters
        ----------
        equation : str-convertible
            The equation string or a string convertible equation object
            to be added.
        """
        eq = self._set_equal_to_zero(equation)
        try:
            eq = parse_expr(eq)
        except:
            raise ValueError('failed to parse equation: {!r}'.format(equation))
        self.equations.append(eq)

    def _set_equal_to_zero(self, equation):
        """
        If the input equations is not an equality, returns the equation string.
        If the equation is an equality, returns an equation string with
        the equality set equal to zero. If the equation has multiple
        equal signs, raise an exception.

        Parameters
        ----------
        equation : str-convertible
            The equation string or an equation object that is convertible to a
            string.
        """
        f = str(equation)
        s = f.split('=')

        if len(s) == 1:
            return f
        elif len(s) == 2:
            return '({})-({})'.format(*s)

        raise ValueError('{!r} contains too many equal signs'.format(equation))

    def _check_values(self, values):
        """
        Checks that the input values satisfy all equations within the
        tolerance assigned to the class. Raises an exception if the tolerance
        is exceeded.

        Parameters
        ----------
        values : dict
            A dictionary mapping variable names to values.
        """
        for i, eq in enumerate(self.equations):
            v = eq.subs(values).evalf()
            try:
                v = float(v)
            except:
                raise ValueError('Equation {}::vars {} are missing in `values` '
                                 'dict'.format(i, v.free_symbols))
            if abs(v) > self.tol:
                raise ValueError('Equation {} value tolerance exceeded:: '
                                 '|{}| > {}'.format(i, v, self.tol))

    def _check_restricted_symbols(self, values, errors):
        """
        Checks that no restricted symbols used by `sympy` are included
        in both the equations and the values and error tolerances dictionaries.

        Parameters
        ----------
        values : dict
            A dictionary mapping variable names to values.
        errors : dict
            A dictionary mapping variable names to error tolerances.
        """
        restr = self.restricted_symbols(values, errors)
        if len(restr) > 0:
            raise ValueError('symbols {} in input dict are restricted and '
                             'cannot be used'.format(restr))

    def check(self, values, errors):
        """
        Checks the input values and error tolerances for errors.

        Parameters
        ----------
        values : dict
            A dictionary mapping variable names to values.
        errors : dict
            A dictionary mapping variable names to error tolerances.
        """
        self._check_restricted_symbols(values, errors)
        self._check_values(values)
        self._check_determinancy(values, errors)

    def equation_variables(self):
        """Returns a set of all variables contained in the equations."""
        eq_vars = set()
        for eq in self.equations:
            eq_vars |= set(map(str, eq.free_symbols))
        return eq_vars

    def restricted_symbols(self, values, errors):
        """
        Returns a set of restricted symbols contained in the equations.

        Parameters
        ----------
        values : dict
            A dictionary mapping variable names to values.
        errors : dict
            A dictionary mapping variable names to error tolerances.
        """
        eq_sym = set()
        for x in self.equations:
            eq_sym |= x.atoms(sympy.NumberSymbol, sympy.I, sympy.zoo)

        symbols = set()
        var = set(values) | set(errors)
        for x in var:
            expr = parse_expr(x)
            symbols |= expr.atoms(sympy.NumberSymbol, sympy.I, sympy.zoo)

        return set(map(str, symbols.intersection(eq_sym)))

    def get_partials(self):
        """
        Returns a list of dictionaries of partial derivatives for the
        class equations.
        """
        partials = []
        for x in self.equations:
            p = {v: sympy.diff(x, v) for v in map(str, x.free_symbols)}
            partials.append(p)
        return partials

    def jacobian(self, values, errors):
        """
        Returns the Jacobian of the system of equations.

        Parameters
        ----------
        values : dict
            A dictionary mapping variable names to values.
        errors : dict
            A dictionary mapping variable names to error tolerances.
        """
        partials = self.get_partials()
        val_vars, err_vars = self.used_variables(values, errors)
        var = {v: i for i, v in enumerate(val_vars + err_vars)}

        m = np.zeros((len(self.equations), len(var)), dtype='float')
        for i, p in enumerate(partials):
            for v in p:
                j = var[v]
                m[i, j] = p[v].subs(values).evalf()
        return m

    def module_str(self, names={}, tab_spaces=4):
        """
        Returns a string for a Python module containing the equations
        and derivatives assigned to the object.

        Parameters
        ----------
        deg : int
            The maximum degree of partial derivatives to be incorporated.
        names : dict
            Variable name substitutions.
        tab_spaces : int
            The number of spaces for tab indents.
        """
        eq = [x.subs(names) for x in self.equations]
        part = self.get_partials()

        for i, x in enumerate(part):
            part[i] = {names[k] if k in names else k:
                       y.subs(names) for k, y in x.items()}

        # Tab
        stab = ' ' * tab_spaces

        # Doc string
        sheader = ['"""',
                   'Error Solver Method Module',
                   '',
                   'Equations:',
                   '{}',
                   '"""',
                   '',
                   'from math import *',
                   '']
        sheader = '\n'.join(sheader)
        s = stab + '{:>' + str(len(str(len(eq)))) + '} : {}'
        s = [s.format(i, e) for i, e in enumerate(eq)]
        s = '\n'.join(s)
        sheader = sheader.format(s)

        # Equations and partials
        seq = ['# Equation {}',
               'def eq{}({}, **kwargs):',
               stab + 'return {}',
               '']
        seq = '\n'.join(seq)

        spart = ['def eq{}_{}({}, **kwargs):',
                 stab + 'return {}',
                 '']
        spart = '\n'.join(spart)

        sbody = []
        for i, x in enumerate(eq):
            args = map(str, x.free_symbols)
            args = ', '.join(args)
            sbody.append(seq.format(i, i, args, x))

            for v, y in part[i].items():
                sbody.append(spart.format(i, v, args, y))
        sbody = '\n'.join(sbody)

        # Assembled equations
        seq = ['# Assembled Methods',
               'def equations():',
               stab + 'return [{}]',
               '']
        seq = '\n'.join(seq)

        sfooter = []
        s = ['eq{}'.format(i) for i in range(len(eq))]
        s = (',\n        ' + stab).join(s)
        sfooter.append(seq.format(s))

        # Assemblied partials
        spart = ['def partials():',
                 stab + 'return [{}]',
                 '']
        spart = '\n'.join(spart)

        sparts = []
        for i, x in enumerate(eq):
            s = ['{!r}: eq{}_{}'.format(v, i, v) for v in map(str, x.free_symbols)]
            s = '{' + ', '.join(s) + '}'
            sparts.append(s)
        sparts = (',\n        ' + stab).join(sparts)
        sfooter.append(spart.format(sparts))
        sfooter = '\n'.join(sfooter)

        return '\n'.join([sheader, sbody, sfooter])

    def write_module(self, path, names={}, tab_spaces=4):
        """
        Writes a Python module containing the equations and derivatives
        assigned to the object to file.

        Parameters
        ----------
        path : str
            The path to which the module will be saved.
        names : dict
            Variable name substitutions.
        tab_spaces : int
            The number of spaces for tab indents.
        """
        s = self.module_str(names, tab_spaces)
        with open(path, 'wt') as fh:
            fh.truncate()
            fh.write(s)
