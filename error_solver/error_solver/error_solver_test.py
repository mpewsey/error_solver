import time
import pytest
from ..data import get_file_path
from .error_solver import *


def test_from_file():
    path = get_file_path('wire_load')
    solver = ErrorSolver.from_file(path)

    assert len(solver.get_equations()) == 4
    assert len(solver.get_partials()) == 4


def test_get_equations():
    path = get_file_path('wire_load')
    solver = ErrorSolver.from_file(path)

    assert len(solver.get_equations('wind_pressure')) == 3
    assert len(solver.get_equations('wind_velocity')) == 4


def test_get_partials():
    path = get_file_path('wire_load')
    solver = ErrorSolver.from_file(path)

    assert len(solver.get_partials('wind_pressure')) == 3
    assert len(solver.get_partials('wind_velocity')) == 4
