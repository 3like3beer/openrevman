from io import StringIO


class Forecaster:
    def __init__(self, remaining_capacity=None, demand_utilization_matrix=None):
        self.parameters = []

    def update_parameter(self):
        self.parameters = 1

    def fit_parameters(self):
        self.parameters = 1

    def forecast(self):
        demand_data = StringIO("1 1 1\n10 20 20")
        demand_utilization_data = StringIO("0 1\n1 0\n1 1")
        return demand_data, demand_utilization_data
