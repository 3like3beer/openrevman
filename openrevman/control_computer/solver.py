#!/usr/bin/python
# -*- coding: utf-8 -*-

import pulp

from numpy import array, loadtxt, ndarray


class Controls:
    def __init__(self, accepted_demand: ndarray, product_bid_prices: ndarray):
        self.accepted_demand = accepted_demand
        self.product_bid_prices = product_bid_prices


class Solver:
    def __init__(self, optimizer):
        self.optimizer = optimizer
        self.controls = None

    def optimize_controls(self, demand_data, price_data, capacity_data, demand_utilization_data):
        self.controls = optimize_controls(demand_data, price_data, capacity_data, demand_utilization_data)
        return self.controls


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
    return Controls(array(accepted_demand), array(product_bid_prices))
