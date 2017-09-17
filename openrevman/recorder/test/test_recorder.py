from unittest import TestCase

from openrevman.recorder.recorder import Record, Recorder


class TestRecord(TestCase):
    def test_get_records(self):
        recorder = Recorder()
        record = Record(products=[1, 4], record_type="Booking")
        self.assertTrue(recorder.get_records == [])
        recorder.record(record)
        self.assertEqual(record, recorder.get_records[0])
        for booking in recorder.get_bookings:
            self.assertEqual(record, booking)
