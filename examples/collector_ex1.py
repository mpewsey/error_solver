# collector_ex1.py
from math import pi
from error_solver import Collector, collect


class Circle(object):
    def __init__(self, r):
        self.r = r

    @collect
    def area(self):
        return pi*self.r**2


# Activate the context manager and make calls to wrapped methods
circle = Circle(2)

with Collector() as collector:
    circle.area()
    collector.get(circle) # {'area': 12.56637}
