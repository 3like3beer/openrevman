from unittest import TestCase

from openrevman.availability_processor.availability_processor import AvailabilityProcessor
from openrevman.control_computer.solver import Controls


class TestAvailabilityProcessor(TestCase):
    def test_get_price(self):
        controls = Controls(accepted_demand=[1,1], product_bid_prices= [3])
        ap = AvailabilityProcessor(controls=controls)
        self.fail()

    def test_is_available(self):
        self.fail()
