import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from price_movement import PriceMovement

class PriceCollection:
    """
    A collection of Price Movements.

    Attributes:
        

    """
    def __init__(self, base_price, price_movement_json):
        self.base_price = base_price
        self.price_movement_json = price_movement_json

    @staticmethod
    def validate_in(price_movement_json):
        schema = {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "num_ticks": {
                        "type": "integer",
                        "minimum": 1
                    },
                    "volatility_window_size": {
                        "type": "number",
                        "minimum": 0.0
                    },
                    "volatility_window_fn": {
                        "type": "string"
                    },
                    "trend_bias": {
                        "type": "number"
                    },
                    "trend_bias_fn": {
                        "type": "string"
                    }
                }
            }
        }

        try:
            validate(price_movement_json, schema)
            return True
        except ValidationError:
            return False

    def get_price_movements(self):
        if not hasattr(self, 'price_movements'):
            self.price_movements = self.generate_price_movements()
        return self.price_movements

    def generate_price_movements(self):
        price_movements = []
        price_movements_config = json.loads(self.price_movement_json)
        base_price = self.base_price

        for price_movement_config in price_movements_config:
            vol_fn = price_movement_config['volatility_window_fn']
            if vol_fn_in == "constant":
                vol_fn = constant_movement
            elif vol_fn_in == "linear":
                vol_fn = linear_movement
            else:
                vol_fn = quadratic_movement

            trend_fn_in = price_movement_config['trend_bias_fn']
            if trend_fn_in == "constant":
                trend_fn = constant_movement
            elif trend_fn_in == "linear":
                trend_fn = linear_movement
            else:
                trend_fn = quadratic_movement

            volatility = price_movement_config['volatility_window_size']
            trend = price_movement_config['trend_bias']
            num_ticks = price_movement_config['num_ticks']

            pm = PriceMovement(self, base_price, num_ticks, 
                vol_fn(volatility, num_ticks), 
                trend_fn(trend, num_ticks))
            
            base_price = pm.get_close_price()
            price_movements.append(pm)

        return price_movements
