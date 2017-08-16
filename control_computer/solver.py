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


def solve_it(demand_data,capa_data):
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html
    demand_matrix = loadtxt(demand_data)
    capa_vector = loadtxt(capa_data)
    # Modify this code to run your optimization algorithm
    value, weight, taken = pulp_solve(demand_matrix, capa_vector)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


def pulp_solve(demand_matrix, capa_vector):
    revman = pulp.LpProblem("revman", pulp.LpMaximize)
    x = [pulp.LpVariable(name="x" + str(i),lowBound= 0,cat= pulp.LpContinuous) for it,i in iter(demand_matrix)]

    objective = pulp.LpAffineExpression([(x[i.index], i.value) for i in demand_matrix])
    revman.setObjective(objective)
    revman += sum([i.weight * x[i.index] for i in demand_matrix]) <= capa_vector - 5
    revman.solve(pulp.COIN_CMD())
    taken = [int(i.value()) for i in x]
    value = sum([demand_matrix[i].value * t for (i, t) in enumerate(taken)])
    weight = sum([demand_matrix[i].weight * t for (i, t) in enumerate(taken)])
    print(weight)
    return value, weight, taken

