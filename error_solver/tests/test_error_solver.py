from error_solver.funcs import percent_change
from error_solver.error_solver import ErrorSolver


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

def test_append_equation():
    equations = ['V = A * h']

    variables = {'h': (12, 0.05),
                 'r': (5, 0.05),
                 'A': (78.54, None),
                 'V': (942.48, None)}

    solver = ErrorSolver(equations, variables)
    solver.append_equation('A = pi * r**2')

    assert solver.check().status

def test_equation_variables():
    equations = ['A = pi * r**2',
                 'V = A * h']

    variables = {'h': (12, 0.05),
                 'r': (5, 0.05),
                 'A': (78.54, None),
                 'V': (942.48, None)}

    solver = ErrorSolver(equations, variables)

    x = tuple(sorted(solver.equation_variables()))
    y = tuple(sorted(['A', 'r', 'V', 'h']))

    assert x==y

def test_unused_variables():
    equations = ['A = pi * r**2',
                 'V = A * h']

    variables = {'h': (12, 0.05),
                 'r': (5, 0.05),
                 'A': (78.54, None),
                 'V': (942.48, None),
                 'B': (1, None),
                 'G': (1, None)}

    solver = ErrorSolver(equations, variables)
    x = tuple(sorted(solver.unused_variables()))
    y = tuple(sorted(['B', 'G']))

    assert x==y

def test_missing_variables():
    equations = ['A = pi * r**2',
                 'V = A * h']

    variables = {'h': (12, 0.05),
                 'r': (5, 0.05)}

    solver = ErrorSolver(equations, variables)
    x = tuple(sorted(solver.missing_variables()))
    y = tuple(sorted(['V','A']))

    assert x==y
