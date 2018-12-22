import os
import time
import pytest
from pytest import approx
from . import error_solver_test
from .error_solver_py import ErrorSolverPy


def module_path():
    path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(path, '_write_module_test2.py')


def write_module():
    solver = error_solver_test.cylinder_error()
    path = module_path()
    solver.write_module(path)


def remove_module():
    path = module_path()
    os.remove(path)

# Write the requisite module
write_module()
time.sleep(2)
from . import _write_module_test2
time.sleep(2)
remove_module()


def cylinder_error_py():
    return ErrorSolverPy.init_from_module(_write_module_test2)


def test_init_from_module():
    solver = cylinder_error_py()
    assert len(solver.equations) == 2
    assert len(solver.partials) == 2


def test_check_values():
    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 900}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = cylinder_error_py()
    with pytest.raises(ValueError) as error:
        solver._check_values(values)


def test_used_variables():
    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 942.48}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = cylinder_error_py()
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

    solver = cylinder_error_py()
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

    solver = cylinder_error_py()
    x = tuple(sorted(solver.unused_variables(values, errors)))
    y = tuple(sorted(['B', 'G']))
    assert x == y


def test_missing_variables():
    values = {'h': 12,
              'r': 5}

    errors = {'h': 0.05,
              'r': 0.05}

    solver = cylinder_error_py()
    x = tuple(sorted(solver.missing_variables(values, errors)))
    y = tuple(sorted(['V', 'A']))
    assert x == y


def test_check_determinancy1():
    solver = cylinder_error_py()

    values = {'h': 12,
              'r': 5,
              'A': 78.54,
              'V': 900}

    errors = {'h': 0.05}

    with pytest.raises(ValueError) as error:
        solver._check_determinancy(values, errors)


def test_check_determinancy2():
    solver = cylinder_error_py()

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

    solver = cylinder_error_py()
    df = solver.solve(values, errors)
    assert approx(df['error']['V'], 0.01) == 22.78
    assert approx(df['pct_error']['V'], 0.01) == 2.42
