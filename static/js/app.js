$(document).ready(function() {
	// socketIO function
	namespace = '/test';
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

	// socket.on('connect', function() {
	// 	socket.emit('my_event', {data: 'I\'m connected!'});
	// });

	socket.on('my_response', function(msg) {
							$('#data_id').text(msg.data_id);
							$('#sensor').text(msg.sensor);
							$('#sensor_value').text(msg.sensor_value);
							$('#date').text(msg.date)

							d3.json("/data",update );
						});
	////////////////////////////////////////////////////////////////////

	
	// draw chart
	var leftPadding = 10;
	var rightPadding = 10;
	var svg = d3.select("svg"),
	width = +svg.attr("width"),
	height = +svg.attr("height"),
	g = svg.append("g")

	function update(data) {
	  var xScale = d3.scaleLinear()
	  				 .domain([d3.min(data, function(d) {return d.data_id;}),
	  				 		d3.max(data, function(d) {return d.data_id;})
	  				 	 ])
	  				.range([0+leftPadding, width-rightPadding]);
	  var yScale = d3.scaleLinear()
	  				 .domain([0,50])
	  				.range([height, 0]);

	  var valueLine = d3.line()
	  					.x(function(d) {return xScale(d.data_id)})
	  					.y(function(d) {return yScale(d.sensor_value)})
	  					.curve(d3.curveMonotoneX);

	  // Draw Path
	  g.selectAll("path").remove();
	  g.append("path")
	  	.datum(data)
	  	.attr("class", "line")
	  	.attr("d", valueLine);

	  //Draw dots on each data point
	  g.selectAll("circle").remove()
	  var dot = g.selectAll("circle")
	  				.data(data, function(d) {
	  					return d;
	  				});
	  dot.enter()
	  	.append("circle")
	  	.attr("class", "dot")
	  	.attr("cx", function(d) {
	  		return xScale(d.data_id);
	  	})
	  	.attr("cy", function(d) {
	  		return yScale(d.sensor_value);
	  	})
	  	.attr("r", 4);

	}
	////////////////////////////////////////////////////////////////////


	$('button').click(function() {
		d3.json("/data",update );
	});	
});