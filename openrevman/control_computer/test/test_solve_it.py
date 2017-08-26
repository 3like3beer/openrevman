from io import StringIO
from unittest import TestCase
from nose.tools import eq_
from openrevman.control_computer import solver


class TestSolve_it(TestCase):
    def test_solve_it(self):
        d = StringIO("5 2")
        p = StringIO("1 20")
        c = StringIO("1 1")
        dud = StringIO("0 1\n2 3")
        result = solver.optimize_controls(demand_data=d, price_data=p,capacity_data=c,demand_utilization_data=dud)
        expected = [3.0, 5.0]
        eq_(expected,result)

    def test_solve_it_single_ressource(self):
        d = StringIO("3 5 4 2 10")
        p = StringIO("10 5 4 2 1")
        c = StringIO("10 10")
        dud = StringIO("1 1\n1 1\n1 1\n1 1\n1 1")
        c = StringIO("10")
        dud = StringIO("1\n1\n1\n1\n1")

        result = solver.optimize_controls(demand_data=d, price_data=p,capacity_data=c,demand_utilization_data=dud)
        expected = [3.0, 5.0, 2.0, 0.0, 0.0]
        eq_(expected, result)


