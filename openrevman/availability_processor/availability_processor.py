class AvailabilityProcessor:
    def __init__(self, controls):
        self.controls = controls

    def get_price(self, product):
        return product * self.controls.product_bid_prices


    def is_available(self, demand):
        return True
