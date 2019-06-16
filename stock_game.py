from flask import Flask
from flask import render_template
from fbm import FBM


import time
import math
import json

NUM_TICKS = 390 # 6.5 hours * 60 minutes

app = Flask(__name__)
app.fbm = FBM(n=NUM_TICKS, hurst=0.75, length=NUM_TICKS, method='daviesharte')
app.fbm_sample = app.fbm.fbm()

@app.route("/")
def index():
    return render_template('main.jnja')

@app.route("/current-prices")
def curr_prices():
    curr_tick = get_current_tick()
    ranges = build_ranges(app.fbm_sample)
    visible_prices = app.fbm_sample[1:curr_tick]
    data = []
    last_price = 0
    curr_sec = 0;

    for visible_price in visible_prices:
        if visible_price > last_price:
            color = "green"
        else:
            color = "red"

        last_price = visible_price
        data.append({'time': curr_sec, 'val': visible_price, 'color': color})
        curr_sec += 1
        

    return json.dumps({'ranges': ranges, 'data': data})

def build_ranges(data):
    max_abs_y = abs(max(data, key=abs))

    ranges = {
        'x': {
            'min': 0,
            'max': NUM_TICKS,
        },
        'y': {
            'min': -max_abs_y,
            'max': max_abs_y,
        },
    }
    return ranges

# Tag data with color
def annotate_data(data):
    return data

def get_current_tick():
    curr_seconds = time.time()
    return int(curr_seconds) % NUM_TICKS

