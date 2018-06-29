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
def eq1(A, V, h, **kwargs):
    return -A*h + V

def eq1_h(A, V, h, **kwargs):
    return -A

def eq1_A(A, V, h, **kwargs):
    return -h

def eq1_V(A, V, h, **kwargs):
    return 1

# Assembled Methods
EQUATIONS = [eq0,
             eq1]

PARTIALS = [{'A' : eq0_A, 'r' : eq0_r},
            {'h' : eq1_h, 'A' : eq1_A, 'V' : eq1_V}]