from io import StringIO
from unittest import TestCase

from nose.tools import eq_, assert_greater_equal
from numpy import array_equal
from pandas import DataFrame

from openrevman.control_computer import solver
from openrevman.control_computer.solver import merge_controls


class TestSolver(TestCase):
    def setUp(self):
        self.three_id_demand = StringIO("1 1 1")
        self.three_prices_latest_large = StringIO("10 10 30")
        self.three_prices_lower_than_two_first = StringIO("10 20 20")
        self.three_id_capacity = StringIO("1 1 1")
        self.two_products_with_capacity_of_one = StringIO("1 1")
        self.demand_utilization_data_three_demand_last_use_two_products = StringIO("0 1\n1 0\n1 1")

    def test_solver_simple_od_od_better(self):
        d = StringIO("1 1 1\n10 10 30")
        c = StringIO("1 1")
        dud = StringIO("0 1\n1 0\n1 1")
        problem = solver.create_problem_with_data(d, c, dud)
        this_solver = solver.Solver(None)
        result = this_solver.optimize_controls(problem)
        expected = DataFrame({'accepted_demand': [0.0, 0.0, 1.0]})
        self.assertTrue(array_equal(expected, result.accepted_demand))
        self.assertTrue(array_equal(30.0, result.expected_revenue))

    def test_solver_simple_od_leg_better(self):
        d = StringIO("1 1 1\n10 20 20")
        c = StringIO("1 1")
        dud = StringIO("0 1\n1 0\n1 1")
        problem = solver.create_problem_with_data(d, c, dud)
        this_solver = solver.Solver(None)
        result = this_solver.optimize_controls(problem)
        expected = DataFrame({'accepted_demand': [1.0, 1.0, 0.0]})
        self.assertTrue(array_equal(expected, result.accepted_demand))
        self.assertTrue(array_equal(30.0, result.expected_revenue))

    def test_solver_single_ressource(self):
        d = StringIO("3 5 4 2 10\n10 5 4 2 1")
        c = StringIO("10")
        dud = StringIO("1\n1\n1\n1\n1")
        problem = solver.create_problem_with_data(d, c, dud)
        this_solver = solver.Solver(None)
        result = this_solver.optimize_controls(problem)

        expected = DataFrame({'accepted_demand': [3.0, 5.0, 2.0, 0.0, 0.0]})
        self.assertTrue(array_equal(expected, result.accepted_demand))
        self.assertTrue(array_equal(63.0, result.expected_revenue))

    def test_problem_get_correlations(self):
        demand_data = StringIO("1 1 1 1\n10 20 20 5")
        capacity_data = self.three_id_capacity
        demand_utilization_data = StringIO("0 1 0\n1 0 0\n1 1 0\n0 0 1")
        problem = solver.create_problem_with_data(demand_data, capacity_data, demand_utilization_data)
        correlations = [[1, 0, 1, 0], [0, 1, 1, 0], [1, 1, 2, 0], [0, 0, 0, 1]]
        self.assertTrue(array_equal(correlations, problem.demand_correlations))

    def test_problem_get_subproblems(self):
        d = StringIO("1 2 2 4\n10 20 20 5")
        c = self.three_id_capacity
        dud = StringIO("0 1 0\n1 0 0\n1 1 0\n0 0 1")

        problem = solver.create_problem_with_data(d, c, dud)
        eq_(problem.get_subproblems().__len__(), 2)
        eq_(problem.get_subproblems()[1].demand_vector.ix[3], 4)
        eq_(problem.get_subproblems()[1].price_vector.ix[3], 5)
        this_solver = solver.Solver(None)

        eq_(this_solver.optimize_controls(problem).expected_revenue,
            this_solver.optimize_controls(problem.get_subproblems()[0]).expected_revenue + 5)
        # this_solver.optimize_controls(problem.get_subproblems()[1]).expected_revenue)

    def test_problem_optimize_controls_multi_period_two_profiles(self):
        d = StringIO("1 2 2 4\n10 20 20 5")
        c = self.three_id_capacity
        dud = StringIO("0 1 0\n1 0 0\n1 1 0\n0 0 1")
        dp = StringIO("1 2 2 4\n0 0 0 0")
        problem = solver.create_problem_with_data(d, c, dud, dp)
        this_solver = solver.Solver(None)

        eq_(this_solver.optimize_controls_multi_period(problem, 0.1).expected_revenue,
            this_solver.optimize_controls(problem).expected_revenue)

    def test_problem_optimize_controls_multi_period_one_profile(self):
        d = StringIO("1 2 2 4\n10 20 20 5")
        c = self.three_id_capacity
        dud = StringIO("0 1 0\n1 0 0\n1 1 0\n0 0 1")
        dp = StringIO("1 2 2 4")
        problem = solver.create_problem_with_data(d, c, dud, dp)
        this_solver = solver.Solver(None)

        eq_(this_solver.optimize_controls_multi_period(problem, 0.1).expected_revenue,
            this_solver.optimize_controls(problem).expected_revenue)

    def test_problem_optimize_controls_multi_period_second_profile_add_val(self):
        d = StringIO("1 0 2 4\n10 20 20 5")
        c = self.three_id_capacity
        dud = StringIO("0 1 0\n1 0 0\n1 1 0\n0 0 1")
        dp = StringIO("0 0 0 0\n1 2 2 4")
        problem = solver.create_problem_with_data(d, c, dud, dp)
        this_solver = solver.Solver(None)

        assert_greater_equal(this_solver.optimize_controls_multi_period(problem, 0.1).expected_revenue,
                             this_solver.optimize_controls(problem).expected_revenue)

    def test_create_problem_with_data(self):
        d = StringIO("1 0 2 4\n10 20 20 5")
        c = self.three_id_capacity
        dud = StringIO("0 1 0\n1 0 0\n1 1 0\n0 0 1")
        dp = StringIO("0 0 0 0\n1 2 2 4")
        problem = solver.create_problem_with_data(d, c, dud, dp)
        eq_(10, problem.price_vector.ix[0, 0])

    def test_merge_controls(self):
        d = StringIO("1 0 2 4\n10 20 20 5")
        c = StringIO("1 1 1")
        dud = StringIO("0 1 0\n1 0 0\n1 1 0\n0 0 1")
        dp = StringIO("0 0 0 0\n1 2 2 4")
        problem = solver.create_problem_with_data(d, c, dud, dp)
        this_solver = solver.Solver(None)

        result1 = this_solver.optimize_controls_multi_period(problem, 0.1).expected_revenue
        sub_controls_list = []
        for p in problem.get_subproblems():
            sub_solver = solver.Solver(None)
            sub_controls_list.append(sub_solver.optimize_controls_multi_period(p, 0.1))

        result2 = merge_controls(sub_controls_list)

        eq_(result1, result2.expected_revenue)
