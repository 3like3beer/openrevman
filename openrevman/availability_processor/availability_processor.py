class AvailabilityProcessor:
    def __init__(self, controls, product_bid_prices):
        self.controls = controls
        self.product_bid_prices = product_bid_prices

    def get_price(self, product):
        return product * self.product_bid_prices


    def is_available(self, demand):
        return True
