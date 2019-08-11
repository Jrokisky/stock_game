const GRID_SIZE = 5;
const MIN_PRICE_DRAW = 2;

$(document).ready(function() {
    $("#add-segment-button").click(function() {
        $new_segment = $("#segments > .segment").first().clone();
        $("#segments").append($new_segment);

        $(".remove-segment-button").click(function() {
            $(this).parent().remove();
        });
    });


	$("#gen-button").click(function() {
        var config = [];
        $("#segments > .segment").each( function(idx, val) {
            ticks = $(this).find('.ticks-in').val();
		    volatility = $(this).find(".volatility-in").val();
		    trend = $(this).find(".trend-in").val();
            vol_fn = $(this).find(".vol-fn-in").val();
            trend_fn = $(this).find(".trend-fn-in").val();

            config.push({
                "num_ticks": Number(ticks),
                "volatility_window_size": Number(volatility),
                "volatility_window_fn": vol_fn,
                "trend_bias": Number(trend),
                "trend_bias_fn": trend_fn,
            });
        });
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: 'current-prices',
            dataType : 'json',
            data: JSON.stringify(config),
            success : data => drawChart(data)
        });
	});
});

function drawChart(data) {
	var canvas = document.getElementById('chart-canvas');
	var width = canvas.width;
	var height = canvas.height;
	var ctx = canvas.getContext("2d");

    // The maximum amount the price will move in any one direction from base_price.
	var max_price_diff = data.ranges.y.max_diff;

	// Background.
	ctx.fillStyle = "black";
	ctx.fillRect(0, 0, canvas.width, canvas.height);

    var base_price = data.data[0].price;
    // center of the canvas should represent the starting price.
    var base_y = height/2;

    // At max, use 80% of the canvas and account for 0,0 being top left.
    var scale_factor = -((base_y*0.8) / max_price_diff);

	for (var i = 0; i < (data.data.length-1); i++) {
		var datum = data.data[i];
        var next_datum = data.data[i+1]

		var price_diff = next_datum.price - datum.price;
        console.log(datum.price);
        console.log(price_diff);
        var color = price_diff > 0 ? 'green' : 'red';

        var rect_x = i * GRID_SIZE;
        var rect_width = GRID_SIZE;
        var rect_y = base_y + ((datum.price - base_price) * scale_factor)
        var rect_height = price_diff * scale_factor;

        // Handle case of small price movement.
        if (rect_height < MIN_PRICE_DRAW && rect_height > 0) {
            rect_height = MIN_PRICE_DRAW;
            color = 'white';
        }
        else if (rect_height > -MIN_PRICE_DRAW && rect_height < 0) {
            rect_height = -MIN_PRICE_DRAW;
            color = 'white';
        }

		ctx.beginPath();
		ctx.rect(rect_x, rect_y, rect_width, rect_height);
		ctx.fillStyle = color;
		ctx.fill();
	}
};

