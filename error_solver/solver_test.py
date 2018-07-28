import os
from pytest import approx
from .solver import ErrorSolver, ErrorSolverPy
from .data import cylinder_error
from .data import DATA_FOLDER


def test_solver():
    equations = ['A = pi * r**2',
                 'V = A * h']

    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = ErrorSolver(equations, values, errors)
    sol = solver.solve()

    assert approx(sol['errors']['V'], 0.01) == 22.78
    assert approx(sol['percent_errors']['V'], 0.01) == 2.42

def test_append_equation():
    equations = ['V = A * h']

    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = ErrorSolver(equations, values, errors)
    solver.append_equation('A = pi * r**2')

    assert solver.check()['ok']

def test_equation_variables():
    equations = ['A = pi * r**2',
                 'V = A * h']

    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = ErrorSolver(equations, values, errors)

    x = tuple(sorted(solver.equation_variables()))
    y = tuple(sorted(['A', 'r', 'V', 'h']))

    assert x == y

def test_unused_variables():
    equations = ['A = pi * r**2',
                 'V = A * h']

    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48,
              'B': 1,
              'G': 2}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = ErrorSolver(equations, values, errors)
    x = tuple(sorted(solver.unused_variables()))
    y = tuple(sorted(['B', 'G']))

    assert x == y

def test_missing_variables():
    equations = ['A = pi * r**2',
                 'V = A * h']

    variables = {'h': (12, 0.05),
                 'r': (5, 0.05)}

    values = {'h': 12,
              'r': 5}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = ErrorSolver(equations, values, errors)
    x = tuple(sorted(solver.missing_variables()))
    y = tuple(sorted(['V', 'A']))

    assert x == y


def test_solver_py():
    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48}

    errors = {'h': 0.05,
              'r': 0.05}

    equations = cylinder_error.equations()
    partials = cylinder_error.partials()

    solver = ErrorSolverPy(equations, partials, values, errors)
    sol = solver.solve()

    assert approx(sol['errors']['V'], 0.01) == 22.78
    assert approx(sol['percent_errors']['V'], 0.01) == 2.42


def test_equation_variables_py():
    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48}

    errors = {'h': 0.05,
              'r': 0.05}

    equations = cylinder_error.equations()
    partials = cylinder_error.partials()

    solver = ErrorSolverPy(equations, partials, values, errors)
    x = tuple(sorted(solver.equation_variables()))
    y = tuple(sorted(['A', 'r', 'V', 'h']))

    assert x == y

def test_write_module():
    equations = ['A = pi * r**2',
                 'V = A * h']

    path = os.path.join(DATA_FOLDER, 'cylinder_error.py')
    solver = ErrorSolver(equations)
    solver.write_module(path)
    os.path.exists(path)

def test_load_module():
    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = ErrorSolverPy.init_from_module(cylinder_error, values, errors)
    sol = solver.solve()

    assert approx(sol['errors']['V'], 0.01) == 22.78
    assert approx(sol['percent_errors']['V'], 0.01) == 2.42
