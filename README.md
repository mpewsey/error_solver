
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
import pandas as pd
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

pd.read_csv(pd.compat.StringIO(solution.summary))
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Variable</th>
      <th>Value</th>
      <th>Error Tolerance</th>
      <th>Percent Error</th>
      <th>Unknown</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>h</td>
      <td>12.000000</td>
      <td>0.050000</td>
      <td>0.416667</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>r</td>
      <td>5.000000</td>
      <td>0.050000</td>
      <td>1.000000</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>78.539816</td>
      <td>1.570796</td>
      <td>2.000000</td>
      <td>True</td>
    </tr>
    <tr>
      <th>3</th>
      <td>V</td>
      <td>942.477796</td>
      <td>22.776547</td>
      <td>2.416667</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>



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

pd.read_csv(pd.compat.StringIO(solution.summary))
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Variable</th>
      <th>Value</th>
      <th>Error Tolerance</th>
      <th>Percent Error</th>
      <th>Unknown</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>h</td>
      <td>12.000000</td>
      <td>0.050000</td>
      <td>0.416667</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>r1</td>
      <td>2.000000</td>
      <td>0.050000</td>
      <td>2.500000</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>r2</td>
      <td>5.000000</td>
      <td>0.050000</td>
      <td>1.000000</td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A1</td>
      <td>12.566371</td>
      <td>0.628319</td>
      <td>5.000000</td>
      <td>True</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A2</td>
      <td>78.539816</td>
      <td>1.570796</td>
      <td>2.000000</td>
      <td>True</td>
    </tr>
    <tr>
      <th>5</th>
      <td>V</td>
      <td>546.637122</td>
      <td>15.472344</td>
      <td>2.830460</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>


