#!/usr/bin/python
# -*- coding: utf-8 -*-

import pulp
from numpy import matrix
from collections import namedtuple

from numpy import loadtxt
import numpy as np

Item = namedtuple("Demand", ['index', 'value', 'used_product'])
Product = namedtuple("Product",['index','capacity'])
Solution= namedtuple("Solution", ['nb_items', 'capacity','taken', 'value','weight'])


def solve_it(demand_data, price_data, capacity_data, demand_utilization_data):
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html

    demand_vector = loadtxt(demand_data)
    price_vector = loadtxt(price_data)
    capacity_vector = loadtxt(capacity_data)
    demand_utilization_matrix  = loadtxt(demand_utilization_data)

    # run optimization algorithm
    value = pulp_solve(demand_vector, price_vector, capacity_vector,demand_utilization_matrix)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    return output_data


def pulp_solve(demand_vector, capacity_vector, price_vector,demand_utilization_matrix):
    revman = pulp.LpProblem("revman", pulp.LpMaximize)
    x = [pulp.LpVariable(name="x" + str(i),lowBound= 0,cat= pulp.LpContinuous) for (i,t) in enumerate(demand_vector)]

    objective = pulp.LpAffineExpression([(x[i.index], price_vector[i.index]) for i in demand_vector])
    revman.setObjective(objective)

    revman += sum([i * x[i.index] for i in demand_utilization_matrix]) <= capacity_vector
    revman += ([x[i] for (i,t) in enumerate(demand_vector)]) <= demand_vector

    revman.solve(pulp.PULP_CBC_CMD())

    accepted_demand = [i.value() for i in x]
    print(accepted_demand)
    return accepted_demand

