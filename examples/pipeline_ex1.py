# pipeline_ex1.py
from error_solver import get_file_path, ErrorSolver, SolverPipeline

solvers = [
    ErrorSolver.from_file(get_file_path('area.ef')),
    ErrorSolver.from_file(get_file_path('volume.ef')),
]

links = [
    {'area': 'area'}
]

values = [
    {'radius': 5, 'area': 78.539816},
    {'height': 12, 'area': 78.539816, 'volume': 942.477796},
]

errors = [
    {'radius': 0.05},
    {'height': 0.05},
]

pipe = SolverPipeline(solvers, links)
pipe.solve(values, errors)
#              value      error  pct_error  is_calc  solver
# var
# area     78.539816   1.570796   2.000000     True       1
# radius    5.000000   0.050000   1.000000    False       1
# area     78.539816   1.570796   2.000000    False       2
# height   12.000000   0.050000   0.416667    False       2
# volume  942.477796  22.776547   2.416667     True       2
