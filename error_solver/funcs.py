"""
===================================================
Miscellaneous Functions (:mod:`error_solver.funcs`)
===================================================

This module contains functions.
"""

def percent_change(x, y):
    """
    Returns the percent change between the input values.

    Parameters:
        * x : float
            First value for which percent change will be calculated relative to.
        * y : float
            Second value.
    """
    return abs(1-y/x)*100 if x!=0 else 0
