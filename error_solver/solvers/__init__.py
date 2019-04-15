"""
==========================================
Error Solver (:mod:`error_solver.solvers`)
==========================================

.. autosummary::
    :toctree: generated/

    ErrorSolver
    ErrorSolverPy
"""

import warnings
from .error_solver_py import *

# Signal a warning if Sympy is not installed
try:
    from .error_solver import *
except ModuleNotFoundError as error:
    if "'sympy'" in str(error):
        warnings.warn('Sympy not installed. Dependent features will not be available.')
    else:
        raise error
except Exception as error:
    raise error

# Clean up namespace
del warnings
