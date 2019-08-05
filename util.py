import math

def linear_movement(magnitude, num_ticks):
    return lambda tick_idx: magnitude * (tick_idx / num_ticks)

def quadratic_movement(magnitude, num_ticks):
    return lambda tick_idx: quadratic(magnitude, num_ticks, tick_idx) 

def quadratic(magnitude, num_ticks, tick_idx):
    progress = tick_idx / num_ticks
    val = math.pow(progress, 2)
    return val * magnitude
