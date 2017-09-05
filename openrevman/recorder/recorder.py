class Recorder:
    def __init__(self):
        self.records = []

    def record(self, new_record):
        self.records.append(new_record)

    @property
    def get_records(self):
        return self.records
