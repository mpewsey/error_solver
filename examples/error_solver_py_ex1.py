# error_solver_py_ex1.py
from error_solver import ErrorSolverPy
from math import pi

# Define the equation functions
def eq0(A, r, **kwargs):
    return A - pi * r**2

def eq0_A(A, r, **kwargs):
    return 1

def eq0_r(A, r, **kwargs):
    return -2*pi*r

def eq1(V, A, h, **kwargs):
    return V - A * h

def eq1_V(V, A, h, **kwargs):
    return 1

def eq1_A(V, A, h, **kwargs):
    return -h

def eq1_h(V, A, h, **kwargs):
    return -A

EQUATIONS = [eq0, eq1]

PARTIALS = [{'A': eq0_A, 'r': eq0_r},
            {'V': eq1_V, 'A': eq1_A, 'h': eq1_h}]

# Solve the equations by some means and assemble the values in a dictionary
values = {
    'h': 12,
    'r': 5,
    'A': 78.54,
    'V': 942.48
}

# Define the known error tolerances
errors = {
    'h': 0.05,
    'r': 0.05
}

solver = ErrorSolverPy(EQUATIONS, PARTIALS)
solver.solve(values, errors)
#           value      error  pct_error  is_calc
# var
# A     78.539816   1.570796   2.000000     True
# V    942.477796  22.776547   2.416667     True
# h     12.000000   0.050000   0.416667    False
# r      5.000000   0.050000   1.000000    False
