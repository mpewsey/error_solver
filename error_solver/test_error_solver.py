from .funcs import percent_change
from .error_solver import ErrorSolver


def test_solver():
    equations = ['A = pi * r**2',
                 'V = A * h']

    variables = {'h': (12, 0.05),
                 'r': (5, 0.05),
                 'A': (78.54, None),
                 'V': (942.48, None)}

    solver = ErrorSolver(equations, variables)
    sol = solver.solve()

    assert percent_change(sol.errors['V'], 22.78)<=1
    assert percent_change(sol.percent_errors['V'], 2.42)<=1
