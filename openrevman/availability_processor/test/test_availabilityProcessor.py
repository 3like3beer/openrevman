from unittest import TestCase

from openrevman.availability_processor.availability_processor import AvailabilityProcessor
from openrevman.control_computer.solver import Controls
from numpy import array


class TestAvailabilityProcessor(TestCase):
    def test_get_price(self):
        controls = Controls(accepted_demand=[1,1], product_bid_prices= [3])
        ap = AvailabilityProcessor(controls=controls)
        demand = array([0,1] )
        assert self.fail()

    def test_is_available(self):
        self.fail()
