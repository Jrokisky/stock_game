from flask import Flask
from flask import render_template
from flask import request
from price_movement import PriceMovement
from util import linear_movement, quadratic_movement

import json

def create_app():
    app = Flask(__name__)
    num_ticks = 30

    @app.route("/")
    def index():
        return render_template('main.jnja')

    @app.route("/current-prices")
    def curr_prices():
        volatility = request.args.get('volatility', 0.25, type=float)
        trend = request.args.get('trend', 0.02, type=float)

        pm = PriceMovement(50.0, num_ticks, 
            linear_movement(volatility, num_ticks), 
            linear_movement(trend, num_ticks))

        print(request.args)
        print(volatility)

        ticks = pm.get_ticks()
        ranges = pm.get_ranges()

        data = []
        last_price = 0
        curr_sec = 0;

        for t in ticks:
            if t.get_open_price() > last_price:
                color = "green"
            else:
                color = "red"

            last_price = t.get_open_price() 
            data.append({'time': curr_sec, 'val': t.get_open_price(), 'color': color})
            curr_sec += 1
        
        return json.dumps({'ranges': ranges, 'data': data})

    return app
