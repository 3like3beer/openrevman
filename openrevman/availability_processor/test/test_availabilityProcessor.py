from unittest import TestCase

from nose.tools import eq_
from numpy import array, ones

from openrevman.availability_processor.availability_processor import AvailabilityProcessor
from openrevman.control_computer.solver import Controls


class TestAvailabilityProcessor(TestCase):
    def test_get_price(self):
        controls = Controls(accepted_demand=array([1, 1]), product_bid_prices=array([3]))
        ap = AvailabilityProcessor(controls=controls, demand_utilization_matrix=ones((2, 1)))
        demand = array([0, 1])
        print(ap.get_price(demand_vector=demand))
        eq_(ap.get_price(demand_vector=demand), 3.0)

    def test_get_price_multi_product(self):
        controls = Controls(accepted_demand=array([1, 1]), product_bid_prices=array([1, 4]))
        ap = AvailabilityProcessor(controls=controls, demand_utilization_matrix=ones((2, 2)))
        demand = array([0, 2])
        print(ap.get_price(demand_vector=demand))
        eq_(ap.get_price(demand_vector=demand), 10.0)

    def test_is_available(self):
        controls = Controls(accepted_demand=array([1, 1]), product_bid_prices=array([3]))
        ap = AvailabilityProcessor(controls=controls, demand_utilization_matrix=ones((2, 1)))
        demand = array([0, 1])
        eq_(ap.is_available(demand_vector=demand), True)

    def test_is_available_not_true(self):
        controls = Controls(accepted_demand=array([1, 1]), product_bid_prices=array([3]))
        ap = AvailabilityProcessor(controls=controls, demand_utilization_matrix=ones((2, 1)))
        demand = array([2, 1])
        eq_(ap.is_available(demand_vector=demand), False)
