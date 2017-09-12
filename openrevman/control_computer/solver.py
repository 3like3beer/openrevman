#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections

import pulp
from numpy import array, loadtxt, ndarray, dot
from scipy.sparse import csgraph


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
        self.demand_correlations = self.get_demand_correlations()

    def get_demand_correlations(self):
        return dot(self.demand_utilization_data, self.demand_utilization_data.transpose())

    def get_subproblems(self, eps=0.1):
        subproblems = []
        labels = csgraph.connected_components(self.demand_correlations, directed=False)[1]
        split_index = collections.Counter(labels).values()
        prev = 0
        for i in split_index:
            demand_data = self.demand_data[prev:i]
            price_data = self.price_data[prev:i]
            capacity_data = self.capacity_data[prev:i]
            subproblems.append(Problem(demand_data, price_data, capacity_data, self.demand_utilization_data))

            # for (label_index, label) in enumerate(labels):
            #         if not last_label == label:
            #             last_label = label
            #             subproblems[label] = self.create_subproblem(label_index, eps)
            #         else:
            #             subproblems[label].add_demand(self, label_index, eps)
        return subproblems

    def add_demand(self, problem, demand_index, eps):
        if problem.demand_data[demand_index] > eps:
            self.demand_data.append(problem.demand_data[demand_index])
            self.price_data.append(problem.price_data[demand_index])
            self.demand_utilization_data.append(problem.demand_utilization_data[demand_index])
        pass

    def create_subproblem(self, demand_index, eps):
        subproblem = Problem([], [], [], demand_utilization_data=self.demand_utilization_data)
        subproblem.add_demand(self, demand_index, eps)
        return subproblem


def dfs(graph, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited


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
