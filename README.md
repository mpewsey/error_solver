
# ERROR SOLVER

## Purpose

This package contains a class for estimating the error tolerances for
a system of equations using the total derivative.

## Installation

This package may be installed via pip:

```
pip install git+https://github.com/line-mind/error_solver#egg=error_solver
```

## Requirements

This package has the following dependencies:

  * `numpy`
  * `sympy`

## Examples

### Import Statements


```python
from error_solver import ErrorSolver
```

### Error in Cylinder

The below example determines the tolerances for the cross sectional area $(A)$ and volume $(V)$ of a cylinder given the measurement tolerances for the radius $(r)$ and height $(h)$.


```python
from math import pi

# Variables     Value         Tolerance (None if unknown to be solved for)
r, rtol     =   5,            0.05
h, htol     =   12,           0.05
A, Atol     =   pi * r**2,    None
V, Vtol     =   A * h,        None

# List of equations.
equations = ['A = pi * r**2',
             'V = A * h']

# Dictionary of variables : (values, tolerances)
variables = {'h': (h, rtol),
             'r': (r, htol),
             'A': (A, Atol),
             'V': (V, Vtol)}

solver = ErrorSolver(equations, variables)
solution = solver.solve()

print(solution.summary)
```

    Variable   Value                     Error Tolerance           Percent Error             Unknown
    h          12                        0.05                      0.4166666666666667               
    r          5                         0.05                      1.0                              
    A          78.53981633974483         1.5707963267948966        2.0                          *   
    V          942.4777960769379         22.776546738526           2.4166666666666665           *   
    

### Error in Tapered Cylinder

The below example determines the tolerances for the cross sectional areas $(A_1, A_2)$ and volume $(V)$ of a cylinder given the measurement tolerances for the radii $(r_1, r_2)$ and height $(h)$.


```python
from math import pi

# Variables     Value             Tolerance (None if unknown to be solved for)
h, htol     =   12,               0.05
r1, r1tol   =   2,                0.05
r2, r2tol   =   5,                0.05
A1, A1tol   =   pi * r1**2,       None
A2, A2tol   =   pi * r2**2,       None
V, Vtol     =   0.5*(A1 + A2)*h,  None

# List of equations.
equations = ['A1 = pi * r1**2',
             'A2 = pi * r2**2',
             'V = 0.5*(A1 + A2)*h']

# Dictionary of variables : (values, tolerances)
variables = {'h' : (h,  htol),
             'r1': (r1, r1tol),
             'r2': (r2, r2tol),
             'A1': (A1, A1tol),
             'A2': (A2, A2tol),
             'V' : (V,  Vtol)}

solver = ErrorSolver(equations, variables)
solution = solver.solve()

print(solution.summary)
```

    Variable   Value                     Error Tolerance           Percent Error             Unknown
    h          12                        0.05                      0.4166666666666667               
    r1         2                         0.05                      2.5                              
    r2         5                         0.05                      1.0                              
    A1         12.566370614359172        0.6283185307179586        5.0                          *   
    A2         78.53981633974483         1.5707963267948966        2.0                          *   
    V          546.637121724624          15.472343818929732        2.830459770114943            *   
    
