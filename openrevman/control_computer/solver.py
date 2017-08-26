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


def optimize_controls(demand_data, price_data, capacity_data, demand_utilization_data):
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html

    demand_vector = loadtxt(demand_data,ndmin=1)
    price_vector = loadtxt(price_data,ndmin=1)
    capacity_vector = loadtxt(fname=capacity_data,ndmin=1)
    print (len(capacity_vector))
    demand_utilization_matrix  = loadtxt(demand_utilization_data,ndmin=2)

    # run optimization algorithm
    value = pulp_solve(demand_vector,capacity_vector, price_vector, demand_utilization_matrix)

    # prepare the solution in the specified output format
    output_data = value
    return output_data


def pulp_solve(demand_vector, capacity_vector, price_vector,demand_utilization_matrix):
    revman = pulp.LpProblem("revman", pulp.LpMaximize)
    x = [pulp.LpVariable(name="x" + str(i),lowBound= 0,cat= pulp.LpContinuous) for (i,t) in enumerate(demand_vector)]

    objective = pulp.LpAffineExpression([(x[i], price_vector[i]) for (i,d) in enumerate(demand_vector)])
    revman.setObjective(objective)
    for (product_index,capacity) in enumerate(capacity_vector):
        revman.addConstraint(pulp.lpSum([x[i] * demand_utilization_matrix[i,product_index] for (i,d) in enumerate(demand_vector)]) <= capacity,name="Capa_" + str(product_index))
    for (i,demand) in enumerate(demand_vector):
        revman.addConstraint((x[i] ) <= demand,name= "Demand_" + str(i))

    revman.solve(pulp.PULP_CBC_CMD())
    revman.writeLP("temp.txt")
    print(pulp.LpStatus[revman.status])
    accepted_demand = [i.value() for i in x]
    print(accepted_demand)

    bp = [revman.constraints.get("Capa_" + str(i)).pi for (i,capacity) in enumerate(capacity_vector)]
    print (bp)
    # for name, c in revman.constraints.items():
    #     print (name, ":", c, "\t", c.pi, "\t\t", c.slack)
    return accepted_demand

