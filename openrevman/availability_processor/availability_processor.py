from numpy import dot, ndarray

from openrevman.control_computer.solver import Controls


class AvailabilityProcessor:
    def __init__(self, controls: Controls, demand_utilization_matrix) -> None:
        """

        :type controls: Controls
        """
        self.controls = controls
        self.demand_utilization_matrix = demand_utilization_matrix

    def get_price(self, demand_vector: ndarray):
        assert self.demand_utilization_matrix.shape[0] == demand_vector.shape[0]
        product_demand = dot(demand_vector, self.demand_utilization_matrix)

        return dot(product_demand, self.controls.product_bid_prices)

    def is_available(self, demand_vector: ndarray):
        return all(demand_vector <= self.controls.accepted_demand)
