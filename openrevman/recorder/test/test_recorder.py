from unittest import TestCase
from openrevman.recorder.recorder import Record
from numpy import array, array_equal
from nose.tools import eq_


class TestRecord(TestCase):
    def test_get_demand_vector(self):
        record = Record(demand=[1, 4], record_type="Booking")
        expected = array([1, 0, 0, 1, 0])
        self.assertTrue(array_equal(expected, record.get_demand_vector(5)))
