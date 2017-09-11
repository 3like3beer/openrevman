#!/usr/bin/python
# -*- coding: utf-8 -*-

import pulp

from numpy import array, loadtxt, ndarray


class Controls:
    def __init__(self, accepted_demand: ndarray, product_bid_prices: ndarray, expected_revenue: float):
        self.accepted_demand = accepted_demand
        self.product_bid_prices = product_bid_prices
        self.expected_revenue = expected_revenue


class Problem:
    def __init__(self, demand_data, price_data, capacity_data, demand_utilization_data):
        self.demand_data = demand_data
        self.price_data = price_data
        self.capacity_data = capacity_data
        self.demand_utilization_data = demand_utilization_data

    def get_subproblems(self):
        root = {}
        for (demand_index, demand) in enumerate(self.demand_data):
            if not root[demand_index]:
                current_root = demand_index
                get_next_demand = 1
        pass

    def add_demand(self, problem, demand_index):
        self.demand_data.add(problem.demand_data[demand_index])
        pass


class Solver:
    def __init__(self, optimizer):
        self.optimizer = optimizer
        self.controls = None

    def optimize_controls(self, demand_data, price_data, capacity_data, demand_utilization_data):
        # separate product (same network iif used by same demand)
        # Finding disjoint Paths in Graphs or cliques
        self.controls = optimize_controls(demand_data, price_data, capacity_data, demand_utilization_data)
        return self.controls

    def optimize_controls_multi_period(self, price_data, demand_data_list, capacity_data, demand_utilization_data, eps):
        for demand_data in demand_data_list:
            if not self.controls:
                ctrl2 = self.optimize_controls(demand_data, price_data, capacity_data, demand_utilization_data)
                if self.compare_with_period(ctrl2, 0.1):
                    self.blinde_control(ctrl2)
            else:
                self.controls = self.optimize_controls(demand_data, price_data, capacity_data, demand_utilization_data)
        return self.controls

    def compare_periods(self, ctrl2, eps):
        rev1 = self.controls.expected_revenue
        if rev1 - ctrl2.expected_revenue > rev1 * eps:
            return True
        return False

    def blinde_control(ctrl2):
        pass


def optimize_controls(demand_data, price_data, capacity_data, demand_utilization_data):
    demand_vector = loadtxt(demand_data, ndmin=1)
    price_vector = loadtxt(price_data, ndmin=1)
    assert price_vector.shape[0] == demand_vector.shape[0]

    capacity_vector = loadtxt(fname=capacity_data, ndmin=1)
    demand_utilization_matrix = loadtxt(demand_utilization_data, ndmin=2)
    assert demand_utilization_matrix.shape[0] == demand_vector.shape[0]
    assert demand_utilization_matrix.shape[1] == capacity_vector.shape[0]

    # run optimization algorithm
    value = pulp_solve(demand_vector, capacity_vector, price_vector, demand_utilization_matrix)

    # prepare the solution in the specified output format
    output_data = value
    return output_data


def pulp_solve(demand_vector, capacity_vector, price_vector, demand_utilization_matrix):
    revman = pulp.LpProblem("revman", pulp.LpMaximize)
    x = [pulp.LpVariable(name="x" + str(i), lowBound=0, cat=pulp.LpContinuous) for (i, t) in enumerate(demand_vector)]

    objective = pulp.LpAffineExpression([(x[i], price_vector[i]) for (i, d) in enumerate(demand_vector)])
    revman.setObjective(objective)
    for (product_index, capacity) in enumerate(capacity_vector):
        revman.addConstraint(pulp.lpSum(
            [x[i] * demand_utilization_matrix[i, product_index] for (i, d) in enumerate(demand_vector)]) <= capacity,
                             name="Capa_" + str(product_index))
    for (i, demand) in enumerate(demand_vector):
        revman.addConstraint((x[i]) <= demand, name="Demand_" + str(i))

    revman.solve(pulp.PULP_CBC_CMD())
    revman.writeLP("temp.txt")
    print(pulp.LpStatus[revman.status])
    accepted_demand = [i.value() for i in x]
    print(accepted_demand)

    product_bid_prices = [revman.constraints.get("Capa_" + str(i)).pi for (i, capacity) in enumerate(capacity_vector)]
    expected_revenue = pulp.value(revman.objective)
    print(expected_revenue)
    return Controls(array(accepted_demand), array(product_bid_prices), expected_revenue)
