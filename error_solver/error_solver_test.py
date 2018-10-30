import os
import time
import pytest
from pytest import approx
from .error_solver import ErrorSolver


def cylinder_error():
    eq = ['A = pi * r**2',
          'V = A * h']
    return ErrorSolver(eq)


def test_add_equation1():
    solver = ErrorSolver([])
    solver.add_equation('V = A * h')
    solver.add_equation('V - A * h')
    assert len(solver.equations) == 2


def test_add_equation2():
    solver = ErrorSolver([])
    with pytest.raises(ValueError) as error:
        solver.add_equation('V = A * h = Z')


def test_add_equation3():
    solver = ErrorSolver([])
    with pytest.raises(ValueError) as error:
        solver.add_equation('JKH*&^*&@#()*')


def test_used_variables():
    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = cylinder_error()
    x_val, x_err = solver.used_variables(values, errors)
    x_val, x_err = tuple(sorted(x_val)), tuple(sorted(x_err))
    y_val, y_err = tuple(sorted(['A', 'V'])), tuple(sorted(['r', 'h']))
    assert x_val == y_val
    assert x_err == y_err


def test_equation_variables():
    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = cylinder_error()
    x = tuple(sorted(solver.equation_variables()))
    y = tuple(sorted(['A', 'r', 'V', 'h']))
    assert x == y


def test_unused_variables():
    values = {'h': 12,
              'B': 1,
              'r': 5,
              'A': 78.54,
              'V': 942.48,
              'G': 2}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = cylinder_error()
    x = tuple(sorted(solver.unused_variables(values, errors)))
    y = tuple(sorted(['B', 'G']))
    assert x == y


def test_missing_variables():
    values = {'h': 12,
              'r': 5}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = cylinder_error()
    x = tuple(sorted(solver.missing_variables(values, errors)))
    y = tuple(sorted(['V', 'A']))
    assert x == y


def test_restricted_symbols():
    values = {'v': 0,
              'I': 0,
              'r': 0,
              'p': 0}

    errors = {'I': 0,
              'r': 0}

    eq = ['v = I * r',
          'p = v * I']

    solver = ErrorSolver(eq)
    x = solver.restricted_symbols(values, errors)
    y = {'I'}
    assert x == y

def test_check_restricted_symbols():
    values = {'v': 0,
              'I': 0,
              'r': 0,
              'p': 0}

    errors = {'I': 0,
              'r': 0}

    eq = ['v = I * r',
          'p = v * I']

    solver = ErrorSolver(eq)
    with pytest.raises(ValueError) as error:
        solver._check_restricted_symbols(values, errors)


def test_check_values1():
    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 900}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = cylinder_error()
    with pytest.raises(ValueError) as error:
        solver._check_values(values)


def test_check_values2():
    values = {'r': 5,
              'A': 78.54,
              'V': 900}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = cylinder_error()
    with pytest.raises(ValueError) as error:
        solver._check_values(values)


def test_check_determinancy1():
    solver = cylinder_error()

    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 900}

    errors = {'h': 0.05}

    with pytest.raises(ValueError) as error:
        solver._check_determinancy(values, errors)


def test_check_determinancy2():
    solver = cylinder_error()

    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 900}

    errors = {'h': 0.05,
              'A': 0.05,
              'r': 0.05}

    with pytest.raises(ValueError) as error:
        solver._check_determinancy(values, errors)


def test_solve():
    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = cylinder_error()
    df = solver.solve(values, errors)
    assert approx(df['error']['V'], 0.01) == 22.78
    assert approx(df['pct_error']['V'], 0.01) == 2.42


def test_module_str():
    solver = cylinder_error()
    solver.module_str()


def test_write_module():
    solver = cylinder_error()
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, '_write_module_test1.py')
    solver.write_module(path)
    time.sleep(2)
    from . import _write_module_test1
    time.sleep(2)
    os.remove(path)
