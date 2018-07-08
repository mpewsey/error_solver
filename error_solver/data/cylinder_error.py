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
def eq1(V, h, A, **kwargs):
    return -A*h + V

def eq1_A(V, h, A, **kwargs):
    return -h

def eq1_V(V, h, A, **kwargs):
    return 1

def eq1_h(V, h, A, **kwargs):
    return -A

# Assembled Methods
def equations():
    return [eq0,
            eq1]

def partials():
    return [{'A' : eq0_A, 'r' : eq0_r},
            {'A' : eq1_A, 'V' : eq1_V, 'h' : eq1_h}]