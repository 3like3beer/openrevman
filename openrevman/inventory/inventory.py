class Inventory:
    def __init__(self, remaining_capacity=None, demand_utilization_matrix=None):
        self.remaining_capacity = remaining_capacity
        self.demand_utilization_matrix = demand_utilization_matrix

    def update_inventory(self,bookings):
        self.remaining_capacity = self.remaining_capacity - bookings.get_products()

