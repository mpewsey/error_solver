"""
===================================================
Error Solver Py (:mod:`civpy.math.error_solver_py`)
===================================================

Contains a class for solving for calculated error tolerances.
"""

import inspect
import numpy as np
from ._base_error_solver import _BaseErrorSolver

__all__ = ['ErrorSolverPy']


class ErrorSolverPy(_BaseErrorSolver):
    """
    Parameters
    ----------
    equations : list
        A list of equation methods.
    partials : dict
        A dictionary of partial derivative equation methods.
    tol : float
        The tolerance used for verifying that values satisfy equations.

    Examples
    --------
    .. literalinclude:: ../examples/error_solver_py_ex1.py

    In lieu of defining the equation methods manually, the :class:`.ErrorSolver`
    class may be used to automatically calculate the partial derivatives
    from an input system of equations and write methods to a Python module
    for use by :class:`ErrorSolverPy`. This can be done as follows:

    .. literalinclude:: ../examples/error_solver_py_ex2.py
    """
    def __init__(self, equations, partials, tol=0.01):
        self.equations = equations
        self.partials = partials
        self.tol = tol

    def init_from_module(module, tol=0.01):
        """
        Parameters
        ----------
        module : module
            An imported module object.
        tol : float
            The tolerance used for verifying that values satisfy equations.
        """
        eq = module.equations()
        part = module.partials()
        return ErrorSolverPy(eq, part, tol)

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
            v = eq(**values)
            if abs(v) > self.tol:
                raise ValueError('Equation {} value tolerance exceeded:: '
                                 '|{}| > {}'.format(i, v, self.tol))

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
        self._check_values(values)
        self._check_determinancy(values, errors)

    def equation_variables(self):
        """Returns a set of all variables contained in the equations."""
        eq_vars = set()
        for eq in self.equations:
            eq_vars |= set(inspect.getargspec(eq)[0])
        return eq_vars

    def get_partials(self):
        """
        Returns a list of dictionaries of partial derivatives for the
        class equations.
        """
        return self.partials

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
        var = val_vars + err_vars

        m = np.zeros((len(self.equations), len(var)), dtype='float')
        for j, p in enumerate(partials):
            for k, v in enumerate(var):
                if v in p: m[j, k] = p[v](**values)
        return m
