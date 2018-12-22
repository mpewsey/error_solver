import numpy as np
import pandas as pd


class _BaseErrorSolver():
    """
    A class with base methods for ErrorSolver and ErrorSolverPy.
    This class has no usage otherwise. See :mod:`civpy.math.error_solver`
    and :mod:`civpy.math.error_solver_py`.
    """
    def used_variables(self, values, errors):
        """
        Returns the variables which are contained in 1) both the values
        dictionary and the equations 2) both the errors dictionary and
        the equations.

        Parameters
        ----------
        values : dict
            A dictionary mapping variable names to values.
        errors : dict
            A dictionary mapping variable names to error tolerances.

        Returns
        -------
        value_variables : list
            A list of variables for which values are known, error tolerances
            are not known, and are present in the equations.
        error_variables : list
            A list of variables for which error tolerances are known and are
            present in the equations.
        """
        eq_vars = self.equation_variables()
        err_vars = eq_vars.intersection(errors)
        val_vars = eq_vars.intersection(values) - err_vars
        return sorted(val_vars), sorted(err_vars)

    def unused_variables(self, values, errors):
        """
        Returns a set of variables for which values and/or error tolerances
        have been passed to the class but which are not included in any
        equations.

        Parameters
        ----------
        values : dict
            A dictionary mapping variable names to values.
        errors : dict
            A dictionary mapping variable names to error tolerances.
        """
        eq_vars = self.equation_variables()
        var = set(values) | set(errors)
        return var - eq_vars

    def missing_variables(self, values, errors):
        """
        Returns a set of variables that are included in the equations
        but which are omitted from both the values and error tolerances
        dictionaries.

        Parameters
        ----------
        values : dict
            A dictionary mapping variable names to values.
        errors : dict
            A dictionary mapping variable names to error tolerances.
        """
        eq_vars = self.equation_variables()
        val_vars, err_vars = self.used_variables(values, errors)
        return eq_vars - set(val_vars) - set(err_vars)

    def _check_determinancy(self, values, errors):
        """
        Checks that the system of equations is determinant. If the system
        is indeterminant, raises an exception.

        Parameters
        ----------
        values : dict
            A dictionary mapping variable names to values.
        errors : dict
            A dictionary mapping variable names to error tolerances.
        """
        val_vars, err_vars = self.used_variables(values, errors)
        n, m = len(val_vars), len(self.equations)

        if n < m:
            raise ValueError('Indeterminant system:: {} equations != {} '
                'unknowns. Consider removing {} errors from vars {} or '
                'changing equations.'.format(m, n, m-n, err_vars))
        elif n > m:
            raise ValueError('Indeterminant system:: {} equations != {} '
                'unknowns. Consider adding {} errors for vars {} or '
                'changing equations.'.format(m, n, n-m, val_vars))

    def solve(self, values, errors):
        """
        Calculates the first order estimated propogation error tolerances
        for the system of equations and returns a DataFrame with the results.
        The unknown error tolerances are calculated using the matrix equation

        .. math:: \Delta X_u = |J_u^{-1}| |J_k| \Delta X_k

        where :math:`J_u^{-1}` is the inverse of the Jacobian for the unknown
        error tolerance variables, :math:`J_k` is the Jacobian of the known
        error tolerance variables, and :math:`\Delta X_k` is a vector of the
        known error tolerances.

        Parameters
        ----------
        values : dict
            A dictionary mapping variable names to values.
        errors : dict
            A dictionary mapping variable names to error tolerances.
        """
        self.check(values, errors)
        val_vars, err_vars = self.used_variables(values, errors)
        n, m = len(val_vars), len(err_vars)
        xk = np.array([errors[k] for k in err_vars], dtype='float')
        xk = np.abs(np.expand_dims(xk, 1))
        mat = self.jacobian(values, errors)
        ju, jk = mat[:,:n], mat[:,-m:]
        jk = np.abs(jk)
        ju = np.abs(np.linalg.inv(ju))

        xu = ju @ (jk @ xk)
        xu = np.asarray(xu.ravel(), dtype='float')

        df = pd.DataFrame()
        df['var'] = val_vars + err_vars
        df['value'] = [values[k] for k in df['var']]
        df['error'] = np.concatenate([xu, [errors[k] for k in err_vars]])
        df['pct_error'] = 100 * abs(df['error'] / df['value'])
        df.replace(float('inf'), np.nan, inplace=True)
        df['is_calc'] = [True] * n + [False] * m
        df.set_index('var', inplace=True)

        return df
