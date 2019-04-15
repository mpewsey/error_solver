# error_solver_ex1.py
from error_solver import ErrorSolver

# Define the equations
EQUATIONS = [
    'A = pi * r**2',
    'V = A * h'
]

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

solver = ErrorSolver(EQUATIONS)
solver.solve(values, errors)
#           value      error  pct_error  is_calc
# var
# A     78.539816   1.570796   2.000000     True
# V    942.477796  22.776547   2.416667     True
# h     12.000000   0.050000   0.416667    False
# r      5.000000   0.050000   1.000000    False
