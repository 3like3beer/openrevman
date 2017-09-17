class Inventory:
    def __init__(self, remaining_capacity=None, products=None):
        self.product_inventory = dict(zip(products, remaining_capacity))

    def update_inventory(self, bookings):
        for booking in bookings:
            for product in booking.products:
                self.product_inventory[product] = self.product_inventory[product] - 1
