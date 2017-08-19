from io import StringIO
from unittest import TestCase

from openrevman.control_computer import solver


class TestSolve_it(TestCase):
    def test_solve_it(self):
        c = StringIO("0 1\n2 3")
        d = StringIO("0 1")
        solver.solve_it(demand_data=c, capa_data=d)
