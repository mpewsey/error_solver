# error_solver_py_ex2.py
from error_solver import ErrorSolver

# Define the equations
EQUATIONS = [
    'A = pi * r**2',
    'V = A * h',
]

# Generate a Python module containing the equations and derived
# partial derivative functions
solver = ErrorSolver(EQUATIONS)
solver.write_python('cylinder_error.py')

# Import the generated module and initialize `ErrorSolverPy` with it
from . import cylinder_error
from error_solver import ErrorSolverPy

solver_py = ErrorSolverPy.from_module(cylinder_error)
