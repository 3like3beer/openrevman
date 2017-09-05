from unittest import TestCase
from openrevman.forecaster.forecaster import Forecaster
from openrevman.control_computer.solver import Solver
from openrevman.inventory.inventory import Inventory
from openrevman.availability_processor.availability_processor import AvailabilityProcessor


class TestSystem(TestCase):
    def setUp(self):
        self.forecaster = Forecaster()
        self.solver = Solver(None)
        self.inventory = Inventory()
        self.ap = AvailabilityProcessor(None, self.inventory.demand_utilization_matrix)

    def test_get_availability(self):
        return self.ap.is_available()

    def test_book(self):

        pass

    def test_get_price(self):
        pass

    def test_update_controls(self):
        self.forecaster.update_parameter()
        self.solver.optimize_controls()
        pass
