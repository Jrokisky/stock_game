from flask import Flask
from flask import render_template
from fbm import FBM
from datetime import datetime

import math
import json

app = Flask(__name__)
data = []
ranges = {
    'x': {
        'min': 0,
        'max': 60,
    },
    'y': {
        'min': -1.2,
        'max': 1.2,
    },
}

@app.route("/")
def index():
    return render_template('main.jnja')

@app.route("/current-prices")
def curr_prices():
    curr_seconds = datetime.now().second
    rad = (curr_seconds * 2 * math.pi) / 60
    val = math.sin(rad)
    color = "green"
    global data

    if len(data) > 0:
        last_datum = data[len(data)-1]

        if curr_seconds < last_datum['time']:
            data.clear()

        if val < last_datum['val']:
            color = "red"
        elif val == last_datum['val']:
            color = last_datum['color']

    data.append({'time': curr_seconds, 'val': val, 'color': color})
    return json.dumps({'ranges': ranges, 'data': data})
