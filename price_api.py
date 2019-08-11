from flask import Flask
from flask import render_template
from flask import request

from price_collection import PriceCollection
from util import get_ranges

import json

def create_app():
    app = Flask(__name__, 
        #TODO:  This should be pulled from config.
            static_url_path="/capital-gains/static")

    num_ticks = 30

    @app.route("/bloomberg")
    def index():
        return render_template('main.jnja')

    @app.route("/current-prices", methods=['POST'])
    def curr_prices():
        data = request.get_json()
        valid = PriceCollection.validate_in(data)

        ticks = []
        price_data = []
        ranges = []
        last_price = 0
        curr_sec = 0;

        if valid:
            p = PriceCollection(100.0, data)
            pms = p.get_price_movements()

            for pm in pms:
                ticks = pm.get_ticks()

                for t in ticks:
                    if t.get_open_price() > last_price:
                        color = "green"
                    else:
                        color = "red"

                    last_price = t.get_open_price() 
                    price_data.append({'time': curr_sec, 'price': t.get_open_price(), 'color': color})
                    curr_sec += 1

        ranges = get_ranges(price_data)
        
        return json.dumps({'ranges': ranges, 'data': price_data})

    return app
