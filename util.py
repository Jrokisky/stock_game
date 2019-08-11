import math

def linear_movement(magnitude, num_ticks):
    return lambda tick_idx: magnitude * (tick_idx / num_ticks)

def constant_movement(magnitude, num_ticks):
    return lambda tick_idx: magnitude

def quadratic_movement(magnitude, num_ticks):
    return lambda tick_idx: quadratic(magnitude, num_ticks, tick_idx) 

def quadratic(magnitude, num_ticks, tick_idx):
    progress = tick_idx / num_ticks
    val = math.pow(progress, 2)
    return val * magnitude

def get_ranges(price_data):
    price_diffs = []
    base_price = price_data[0]['price']
    for price_datum in price_data:
        price_diffs.append(price_datum['price'] - base_price)

    max_diff = abs(max(price_diffs, key=abs))    

    ranges = {
        'x': {
            'min': 0,
            'max': len(price_data),
        },
        'y': {
            'max_diff': max_diff,
        },
    }
    return ranges
