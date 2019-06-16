const grid_size = 5;

function getData() {
	$.getJSON("/current-prices", function(data) {
		drawChart(data);
	});
};

function drawChart(data) {
	var canvas = document.getElementById('chart-canvas');
	var width = canvas.width;
	var height = canvas.height;
	var ctx = canvas.getContext("2d");

	var min_x = data.ranges.x.min
	var max_x = data.ranges.x.max
	var min_y = data.ranges.y.min
	var max_y = data.ranges.y.max

	// Background.
	ctx.fillStyle = "black";
	ctx.fillRect(0, 0, canvas.width, canvas.height);

	for (var i = 0; i < data.data.length; i++) {
		var datum = data.data[i];
		var y = height - get_coord(min_y, max_y, height, datum.val);
		var x = get_coord(min_x, max_x, width, datum.time);

		var quot_x = Math.floor(x/grid_size);
		var quot_y = Math.floor(y/grid_size);
		var grid_x = quot_x * grid_size;
		var grid_y = quot_y * grid_size;

		ctx.beginPath();
		ctx.rect(grid_x, grid_y, grid_size, grid_size);
		ctx.fillStyle = datum.color;
		ctx.fill();
	}
};

function get_coord(min, max, dim, val) {
	var span = max - min;
	return ((val - min) * dim) / span;
};

window.setInterval(function() {
	getData();
}, 500);


