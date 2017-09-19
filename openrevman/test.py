from unittest import TestCase

from openrevman.availability_processor.availability_processor import AvailabilityProcessor
from openrevman.control_computer.solver import Solver, create_problem_with_df
from openrevman.forecaster.forecaster import Forecaster
from openrevman.inventory.inventory import Inventory
from openrevman.recorder.recorder import Record
from openrevman.recorder.recorder import Recorder


class TestSystem(TestCase):
    def setUp(self):
        self.forecaster = Forecaster()
        self.solver = Solver(None)
        self.inventory = Inventory(products=["p1", "p2"], remaining_capacity=[10, 10])
        self.recorder = Recorder()
        self.ap = AvailabilityProcessor(None, None)

    def test_get_availability(self):
        # return self.ap.is_available()
        pass

    def test_book(self):
        booking = Record(record_type="Booking", products=["p1"])
        self.recorder.record(booking)
        self.inventory.update_inventory(bookings=[booking])
        assert self.inventory.product_inventory["p1"] == 9
        assert self.inventory.product_inventory["p2"] == 10
        pass

    def test_updateparameter(self):
        self.forecaster.update_parameter()
        pass

    def test_get_price(self):
        pass

    def test_update_controls(self):
        demand_data, demand_utilization_data = self.forecaster.forecast()
        capacity_data = self.inventory.get_capacity()

        problem = create_problem_with_df(demand_data, capacity_data, demand_utilization_data)
        self.solver.optimize_controls(problem)
        # self.ap.controls = self.solver.controls
        pass
