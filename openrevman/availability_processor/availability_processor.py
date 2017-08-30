from openrevman.control_computer.solver import Controls
from numpy import ndarray

class AvailabilityProcessor:
    def __init__(self, controls: Controls, demand_utilization_matrix) -> object:
        self.controls = controls
        self.demand_utilization_matrix = demand_utilization_matrix

    def get_price(self, demand:ndarray):
        return demand * self.demand_utilization_matrix * self.controls.product_bid_prices

    def is_available(self, demand:ndarray):
        return demand < self.controls.accepted_demand
