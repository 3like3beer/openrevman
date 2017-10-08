#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections

import pulp
from numpy import dot
from pandas import DataFrame, read_table
from scipy.sparse import csgraph


class Controls:
    def __init__(self, accepted_demand: DataFrame, product_bid_prices: DataFrame, expected_revenue: float = None):
        self.accepted_demand = accepted_demand
        self.product_bid_prices = product_bid_prices
        self.expected_revenue = expected_revenue


class Problem:
    def __init__(self, demand_vector, price_vector, capacity_vector, demand_utilization_matrix, demand_profile=None):
        self.demand_vector = demand_vector
        self.price_vector = price_vector
        self.capacity_vector = capacity_vector
        self.demand_utilization_matrix = demand_utilization_matrix
        self.demand_profile = demand_profile
        self.demand_correlations = self.get_demand_correlations()

    def get_demand_correlations(self):
        return dot(self.demand_utilization_matrix, self.demand_utilization_matrix.transpose())

    def get_subproblems(self, eps=0.1):
        subproblems = []
        labels = csgraph.connected_components(self.demand_correlations, directed=False)[1]
        split_index = collections.Counter(labels).values()
        prev = 0
        for i in split_index:
            demand_vector = self.demand_vector[prev:prev + i]
            price_vector = self.price_vector[prev:prev + i]
            capacity_vector = self.capacity_vector
            demand_utilization_matrix = self.demand_utilization_matrix.ix[prev:prev + i, :]
            demand_profile = None
            if self.demand_profile is not None:
                demand_profile = self.demand_profile.ix[prev:prev + i - 1, :]
            subproblems.append(
                Problem(demand_vector=demand_vector, price_vector=price_vector, capacity_vector=capacity_vector,
                        demand_utilization_matrix=demand_utilization_matrix, demand_profile=demand_profile))
            prev = i
        return subproblems


class Solver:
    def __init__(self, optimizer):
        self.optimizer = optimizer
        self.controls = None

    def optimize_controls(self, problem):
        self.controls = pulp_solve(problem.demand_vector, problem.price_vector, problem.capacity_vector,
                                   problem.demand_utilization_matrix)
        return self.controls

    def optimize_controls_multi_period(self, problem, eps):
        if problem.demand_profile.shape[1] > 1:
            for period in problem.demand_profile.columns:
                if self.controls:
                    new_control = pulp_solve(problem.demand_profile.ix[:, period], problem.price_vector,
                                             problem.capacity_vector,
                                             problem.demand_utilization_matrix)
                    if self.is_new_ctrl_more_profitable(new_control, 0.1):
                        self.blinde_control(new_control, eps)
                else:
                    self.controls = self.optimize_controls(problem)
        else:
            self.controls = self.optimize_controls(problem)
        return self.controls

    def is_new_ctrl_more_profitable(self, new_control, eps):
        rev1 = self.controls.expected_revenue
        if new_control.expected_revenue - rev1 > rev1 * eps:
            return True
        return False

    def blinde_control(self, new_control, eps):
        self.controls.accepted_demand = self.controls.accepted_demand * eps
        self.controls.product_bid_prices = self.controls.product_bid_prices / eps
        self.controls.expected_revenue = new_control.expected_revenue


def to_data_frame(data):
    df = DataFrame.transpose(read_table(data, delim_whitespace=True, header=None))
    df.columns = [(col + 1) for col in df.columns]
    return df


def to_data_frame2(data):
    df = DataFrame(read_table(data, delim_whitespace=True, header=None))
    return df


def create_problem_with_data(demand_data, capacity_data, demand_utilization_data, demand_profile_data=None):
    demand_vector, capacity_vector, demand_profile, demand_utilization_matrix = load_data_to_df(capacity_data,
                                                                                                demand_data,
                                                                                                demand_profile_data,
                                                                                                demand_utilization_data)
    return Problem(demand_vector.ix[:, 1], demand_vector.ix[:, 2], capacity_vector,
                   demand_utilization_matrix.ix[:, :],
                   demand_profile)


def merge_controls(controls_list):
    first_time = True
    for controls in controls_list:
        if first_time:
            accepted_demand = controls.accepted_demand
            product_bid_prices = controls.product_bid_prices
            expected_revenue = controls.expected_revenue
            first_time = False
        else:
            accepted_demand = accepted_demand.append(controls.accepted_demand)
            product_bid_prices = product_bid_prices.append(controls.product_bid_prices)
            expected_revenue = expected_revenue + controls.expected_revenue

    return Controls(accepted_demand=accepted_demand, product_bid_prices=product_bid_prices,
                    expected_revenue=expected_revenue)


def load_data_to_df(capacity_data, demand_data, demand_profile_data, demand_utilization_data):
    demand_vector = to_data_frame(demand_data)
    capacity_vector = to_data_frame(capacity_data)
    demand_utilization_matrix = to_data_frame2(demand_utilization_data)
    assert demand_utilization_matrix.shape[0] == demand_vector.shape[0]
    assert demand_utilization_matrix.shape[1] == capacity_vector.shape[0]
    if demand_profile_data:
        demand_profile = to_data_frame(demand_profile_data)
        assert demand_profile.shape[0] == demand_vector.shape[0]
    else:
        demand_profile = None
    return demand_vector, capacity_vector, demand_profile, demand_utilization_matrix


def pulp_solve(demand_vector, price_vector, capacity_vector, demand_utilization_matrix):
    revman = create_problem()
    x = create_variables(demand_vector)
    set_objective(demand_vector, price_vector, revman, x)
    add_product_constraints(capacity_vector, demand_utilization_matrix, demand_vector, revman, x)
    add_demand_constraints(demand_vector, revman, x)

    solve_problem(revman)

    accepted_demand = get_accepted_demand(x)
    product_bid_prices = get_bid_prices(capacity_vector, revman)
    expected_revenue = get_expected_revenue(revman)

    return Controls((accepted_demand), (product_bid_prices), expected_revenue)


def solve_problem(revman):
    revman.solve(pulp.PULP_CBC_CMD())
    # revman.writeLP("temp.txt")
    # print(pulp.LpStatus[revman.status])


def create_problem():
    return pulp.LpProblem("revman", pulp.LpMaximize)


def get_expected_revenue(revman):
    return pulp.value(revman.objective)


def get_accepted_demand(x):
    return DataFrame({'accepted_demand': [(x[str(i)].value()) for i in x]})


def get_bid_prices(capacity_vector, revman):
    bid_prices_list = [revman.constraints.get("Capa_" + str(i)).pi for (i, c) in (capacity_vector.iterrows())]
    return DataFrame({'bid_prices_list': bid_prices_list})


def add_demand_constraints(demand_vector, revman, x):
    for (demand_index, demand) in (demand_vector.iteritems()):
        revman.addConstraint((x[str(demand_index)]) <= demand, name="Demand_" + str(demand_index))


def add_product_constraints(capacity_vector, demand_utilization_matrix, demand_vector, revman, x):
    for (product_index, capacity) in (capacity_vector.iterrows()):
        revman.addConstraint(pulp.lpSum(
            [x[str(i)] * demand_utilization_matrix.ix[i, product_index] for (i, d) in demand_vector.iteritems()]) <=
                             capacity,
                             name="Capa_" + str(product_index))


def set_objective(demand_vector, price_vector, revman, x):
    objective = pulp.LpAffineExpression([(x[str(i)], price_vector[i]) for (i, d) in demand_vector.iteritems()])
    revman.setObjective(objective)


def create_variables(demand_vector):
    x = dict([(str(i), pulp.LpVariable(name="x" + str(i), lowBound=0, cat=pulp.LpContinuous)) for (i, t) in
              demand_vector.iteritems()])
    return x
