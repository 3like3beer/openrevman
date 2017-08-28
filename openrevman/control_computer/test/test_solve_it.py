from io import StringIO
from unittest import TestCase
from nose.tools import eq_
from openrevman.control_computer import solver


class TestSolve_it(TestCase):
    def test_solve_it_simple_od_od_better(self):
        d = StringIO("1 1 1")
        p = StringIO("10 10 30")
        c = StringIO("1 1")
        dud = StringIO("0 1\n1 0\n1 1")
        result = solver.optimize_controls(demand_data=d, price_data=p, capacity_data=c, demand_utilization_data=dud)
        expected = [0.0, 0.0, 1.0]
        eq_(expected, result.accepted_demand)

    def test_solve_it_simple_od_leg_better(self):
        d = StringIO("1 1 1")
        p = StringIO("10 20 20")
        c = StringIO("1 1")
        dud = StringIO("0 1\n1 0\n1 1")
        result = solver.optimize_controls(demand_data=d, price_data=p, capacity_data=c, demand_utilization_data=dud)
        expected = [1.0, 1.0, 0.0]
        eq_(expected, result.accepted_demand)

    def test_solve_it_single_ressource(self):
        d = StringIO("3 5 4 2 10")
        p = StringIO("10 5 4 2 1")
        c = StringIO("10 10")
        dud = StringIO("1 1\n1 1\n1 1\n1 1\n1 1")
        c = StringIO("10")
        dud = StringIO("1\n1\n1\n1\n1")

        result = solver.optimize_controls(demand_data=d, price_data=p,capacity_data=c,demand_utilization_data=dud)
        expected = [3.0, 5.0, 2.0, 0.0, 0.0]
        eq_(expected, result.accepted_demand)


