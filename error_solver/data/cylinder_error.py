"""
Error Solver Function Module

Equations:
    0 : A - pi*r**2
    1 : -A*h + V
"""

from math import *

# Equation 0
def eq0(r, A, **kwargs):
    return A - pi*r**2

def eq0_A(r, A, **kwargs):
    return 1

def eq0_r(r, A, **kwargs):
    return -2*pi*r

# Equation 1
def eq1(h, V, A, **kwargs):
    return -A*h + V

def eq1_V(h, V, A, **kwargs):
    return 1

def eq1_A(h, V, A, **kwargs):
    return -h

def eq1_h(h, V, A, **kwargs):
    return -A

# Assembled Methods
def equations():
    return [eq0,
            eq1]

def partials():
    return [{'A' : eq0_A, 'r' : eq0_r},
            {'V' : eq1_V, 'A' : eq1_A, 'h' : eq1_h}]
