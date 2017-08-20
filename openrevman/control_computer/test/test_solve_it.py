from io import StringIO
from unittest import TestCase

from openrevman.control_computer import solver


class TestSolve_it(TestCase):
    def test_solve_it(self):
        d = StringIO("5 2")
        p = StringIO("1 2")
        c = StringIO("1 1")
        dud = StringIO("0 1\n2 3")
        solver.solve_it(demand_data=d, price_data=p,capacity_data=c,demand_utilization_data=dud)
