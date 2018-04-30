"""
===================================================
Miscellaneous Functions (:mod:`error_solver.funcs`)
===================================================

This module contains functions.
"""

import sys


def percent_change(x, y):
    """
    Returns the percent change between the input values.

    Parameters:
        * x : float
            First value for which percent change will be calculated relative to.
        * y : float
            Second value.
    """
    if x==0:
        x = sys.float_info.min

    return abs(1-y/x)*100
