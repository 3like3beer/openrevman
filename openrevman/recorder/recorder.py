from numpy import ndarray

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
        return self.filter_by_type("bookings")

    def filter_by_type(self, value) -> object:
        for record in self.records:
            if record.type == value:
                yield record


class Record:
    def __init__(self, record_type, demand):
        """

        :param record_type: type of record
        :param products: list of products used by record
        """
        self.type = record_type
        self.demand = demand

    def get_demand_vector(self):
        return ndarray()


