#!/usr/bin/python
# -*- coding: utf-8 -*-

import pulp
from numpy import matrix
from collections import namedtuple

from numpy import loadtxt

Item = namedtuple("Demand", ['index', 'value', 'used_product'])
Product = namedtuple("Product",['index','capacity'])
Solution= namedtuple("Solution", ['nb_items', 'capacity','taken', 'value','weight'])


def solve_it(demand_data,capa_data):
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html
    demand_matrix = loadtxt(capa_data)
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = demand_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value, weight, taken = pulp_solve(items, capacity)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


def pulp_solve(items, capacity):
    knapsack = pulp.LpProblem("Knapsack Model", pulp.LpMaximize)
    x = [pulp.LpVariable("x" + str(it.index), 0, 1, 'Integer') for it in items]

    objective = pulp.LpAffineExpression([(x[i.index], i.value) for i in items])
    knapsack.setObjective(objective)
    knapsack += sum([i.weight * x[i.index] for i in items]) <= capacity - 5
    knapsack.solve(pulp.COIN_CMD())
    taken = [int(i.value()) for i in x]
    value = sum([items[i].value * t for (i, t) in enumerate(taken)])
    weight = sum([items[i].weight * t for (i, t) in enumerate(taken)])
    print(weight)
    return value, weight, taken

