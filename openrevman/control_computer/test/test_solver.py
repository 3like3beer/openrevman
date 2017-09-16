from io import StringIO
from unittest import TestCase

from nose.tools import eq_
from numpy import array, array_equal, loadtxt

from openrevman.control_computer import solver


class TestSolver(TestCase):
    def test_solver_simple_od_od_better(self):
        d = StringIO("1 1 1")
        p = StringIO("10 10 30")
        c = StringIO("1 1")
        dud = StringIO("0 1\n1 0\n1 1")
        result = solver.optimize_controls(demand_data=d, price_data=p, capacity_data=c, demand_utilization_data=dud)
        expected = array([0.0, 0.0, 1.0])
        self.assertTrue(array_equal(expected, result.accepted_demand))
        self.assertTrue(array_equal(30.0, result.expected_revenue))

    def test_solver_simple_od_leg_better(self):
        d = StringIO("1 1 1")
        p = StringIO("10 20 20")
        c = StringIO("1 1")
        dud = StringIO("0 1\n1 0\n1 1")
        result = solver.optimize_controls(demand_data=d, price_data=p, capacity_data=c, demand_utilization_data=dud)
        expected = array([1.0, 1.0, 0.0])
        self.assertTrue(array_equal(expected, result.accepted_demand))
        self.assertTrue(array_equal(30.0, result.expected_revenue))

    def test_solver_single_ressource(self):
        d = StringIO("3 5 4 2 10")
        p = StringIO("10 5 4 2 1")
        c = StringIO("10")
        dud = StringIO("1\n1\n1\n1\n1")
        result = solver.optimize_controls(demand_data=d, price_data=p, capacity_data=c, demand_utilization_data=dud)
        expected = array([3.0, 5.0, 2.0, 0.0, 0.0])
        self.assertTrue(array_equal(expected, result.accepted_demand))
        self.assertTrue(array_equal(63.0, result.expected_revenue))

    def test_problem_get_correlations(self):
        demand_data = StringIO("1 1 1 1")
        price_data = StringIO("10 20 20 5")
        capacity_data = StringIO("1 1 1")
        demand_utilization_data = StringIO("0 1 0\n1 0 0\n1 1 0\n0 0 1")
        d = loadtxt(demand_data, ndmin=1)
        p = loadtxt(price_data, ndmin=1)
        c = loadtxt(fname=capacity_data, ndmin=1)
        dud = loadtxt(demand_utilization_data, ndmin=2)

        problem = solver.Problem(demand_vector=d, price_vector=p, capacity_vector=c, demand_utilization_matrix=dud)
        print("correlations")
        print(problem.demand_correlations)

    def test_problem_get_subproblems(self):
        d = StringIO("1 2 2 4")
        p = StringIO("10 20 20 5")
        c = StringIO("1 1 1")
        dud = StringIO("0 1 0\n1 0 0\n1 1 0\n0 0 1")

        problem = solver.create_problem(d, p, c, dud)
        eq_(problem.get_subproblems().__len__(), 2)
        eq_(problem.get_subproblems()[1].demand_vector, [4])
        eq_(problem.get_subproblems()[1].price_vector, [5])
        this_solver = solver.Solver(None)

        eq_(this_solver.optimize_controls(problem).expected_revenue,
            this_solver.optimize_controls(problem.get_subproblems()[0]).expected_revenue +
            this_solver.optimize_controls(problem.get_subproblems()[1]).expected_revenue)

    def test_problem_optimize_controls_multi_period(self):
        d = StringIO("1 2 2 4")
        p = StringIO("10 20 20 5")
        c = StringIO("1 1 1")
        dud = StringIO("0 1 0\n1 0 0\n1 1 0\n0 0 1")

        problem = solver.create_problem(d, p, c, dud)
        this_solver = solver.Solver(None)

        eq_(this_solver.optimize_controls_multi_period(problem, 0.1).expected_revenue,
            this_solver.optimize_controls(problem).expected_revenue)
