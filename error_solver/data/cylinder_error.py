"""
Error Solver Function Module

Equations:
    0 : A - pi*r**2
    1 : -A*h + V
"""

from math import *

# Equation 0
def eq0(A, r, **kwargs):
    return A - pi*r**2

def eq0_A(A, r, **kwargs):
    return 1

def eq0_r(A, r, **kwargs):
    return -2*pi*r

# Equation 1
def eq1(A, h, V, **kwargs):
    return -A*h + V

def eq1_A(A, h, V, **kwargs):
    return -h

def eq1_h(A, h, V, **kwargs):
    return -A

def eq1_V(A, h, V, **kwargs):
    return 1

# Assembled Methods
def equations():
    return [eq0,
            eq1]

def partials():
    return [{'A' : eq0_A, 'r' : eq0_r},
            {'A' : eq1_A, 'h' : eq1_h, 'V' : eq1_V}]