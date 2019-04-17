# collector_ex2.py
from math import pi
from error_solver import Collector, fcollect


@fcollect
def area(r):
    return pi*r**2


# Activate the context manager and make calls to wrapped functions
with Collector() as collector:
    area(2)
    collector.fget(area) # 12.56637
