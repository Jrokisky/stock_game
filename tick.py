from random import uniform

class Tick:
    """
    The smallest unit of price movement.

    Attributes:
        open_price (0 < float): opening price of the tick
        window_size (0 < float < 1.0): per direction size of volatility window
        window_bias (-1.0 < float < 1.0): amount to bias opening price
    """

    def __init__(self, open_price, window_size, window_bias):
        self.open_price = open_price
        self.window_size = window_size
        self.window_bias = window_bias

    def get_open_price(self):
        return self.open_price

    def get_close_price(self):
        if not hasattr(self, 'close_price'):
            self.close_price = self.compute_close_price()
        return self.close_price

    def compute_close_price(self):
        biased_open_price = self.open_price * (1 + self.window_bias)
        window_size_absolute = biased_open_price * self.window_size
        max_close_price = biased_open_price + window_size_absolute
        min_close_price = biased_open_price - window_size_absolute
        return uniform(min_close_price, max_close_price)
