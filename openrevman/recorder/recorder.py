class Recorder:
    def __init__(self):
        self.records = []

    def record(self, new_record):
        self.records.append(new_record)

    @property
    def get_records(self):
        return self.records

    @property
    def get_bookings(self):
        return self.filter_by_type("Booking")

    def filter_by_type(self, value) -> object:
        for record in self.records:
            if record.type == value:
                yield record


class Record:
    def __init__(self, record_type, products):
        """

        :param record_type: type of record
        :param demand: list of demands for the record
        """
        self.type = record_type
        self.products = products
