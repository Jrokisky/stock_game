import math
from random import uniform
from tick import Tick

class PriceMovement:
    """
    A collection of Ticks.

    Attributes:
        open_price(0 < float): opening price 
        num_ticks( 0 < int): number of ticks
        window_size_fn(tick_idx => window_size): maps tick index volatilty window size
        window_bias_fn(tick_idx => window_bias): maps tick index to window bias
    """

    def __init__(self, open_price, num_ticks, window_size_fn, window_bias_fn):
        self.open_price = open_price
        self.num_ticks = num_ticks
        self.window_size_fn = window_size_fn
        self.window_bias_fn = window_bias_fn

    def get_ticks(self):
        if not hasattr(self, 'ticks'):
            self.ticks = self.generate_ticks()
        return self.ticks

    def generate_ticks(self):
        ticks = []
        base_tick = Tick(self.open_price, self.window_size_fn(0), 
                        self.window_bias_fn(0))
        ticks.append(base_tick)

        for x in range(1, self.num_ticks):
            prev_tick = ticks[x-1]
            prev_tick_close = prev_tick.get_close_price()
            nxt_tick = Tick(prev_tick_close, self.window_size_fn(x), 
                            self.window_bias_fn(x))
            ticks.append(nxt_tick)

        return ticks
    
    def get_close_price(self):
        if not hasattr(self, 'ticks'):
            self.ticks = self.generate_ticks()
        return self.ticks[-1].get_close_price()       
