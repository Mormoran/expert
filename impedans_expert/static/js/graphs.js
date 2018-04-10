$(document).ready(function() {
	var algorithm_run_id = -1;
	try {
		var is_advanced_select = advanced_select;
	} catch(err) {
		var is_advanced_select = -1;
	};
	if (Boolean(is_advanced_select)) {
		// run advanced algorithm selection
		// try {
		// 	algorithm_id = algorithm_id;
		// } catch(err) {
		// 	algorithm_id = -1;
		// };
		// try {
		// 	mode = mode;
		// } catch(err) {
		// 	var algorithm_id = -1;
		// }; 
		// if (algorithm_id != -1) {
		// 	var algorithm_runs_url_string = "/expert/api/algorithm-run/?algorithm=" + algorithm_id.toString() + "&customer=" + customer + "&format=json";
		// 	getAlgorithmRuns(algorithm_runs_url_string);
		// 	// getJSON data:
		// 	// Step 1: algorithm_run where algorithm_id = algorithm_id
		// 	//
		// 	// if mode = time
		// 	//     Step 2: algorithm_time_results where algorithm_run_id__in=algorithm_run_id, chamber=chamber_id, parameter=parameter_id
		// 	// else
		// 	//     Step 2: runs where chamber=chamber
		// 	//     Step 3: algorithm_run_results where algorithm_run_id__in=algorithm_run_id, runs__in=runs, parameter=parameter_id
		// }
	} else {
		try {
			var algorithm_run_id = algorithm_run_valid_id;
		} catch(err) {
			var algorithm_run_id = -1;
		};
        var algorithm_run_id_str = algorithm_run_id.toString();
        var url_string = "/expert/api/algorithm-time-results/?algorithm_run=" + algorithm_run_id_str + "&ordering=start_time" + "&format=json";
		getLineChartData(url_string);		
	};
	

	///////////////////////////////////////////////////////////////////////////////////////////////
	// Define a function to programmatically calculate the width of the bounding box for charts  //
	///////////////////////////////////////////////////////////////////////////////////////////////

	function getInnerWidth(elem) {
		return parseFloat(window.getComputedStyle(elem).width);
	};

	var target_element = document.getElementById("navbarExpertMenu");
	var graph_width = getInnerWidth(target_element);


	///////////////////////////////////////////////////////////////////////////////////////////////
	// Define a function to retrieve data points, values and dates for the scatter plot.		 //
	// It takes in a URL string as argument. It queries the API for AlgorithmRunResults data.	 //
	///////////////////////////////////////////////////////////////////////////////////////////////

	function convertCollectionElement(input, index) {
		return {
		  "x": index,
		  "y": input.value,
		  "z": input.start_time
		};
	};
	
	function convertCollection(inputs) {
		return inputs.map(convertCollectionElement);
	};

	function getScatterPlotRunData(url_string) {
		$.getJSON(url_string, function(data) {
			var scatter_data = convertCollection(data);
			param_name = data[0].parameter
			console.log("-------------------------");
			console.log(scatter_data);
			console.log("-------------------------");
			drawScatterPlot(scatter_data, param_name);
		});
	};


	////////////////////////////////////////////////////////////////////////////////////////////////
	// Define a function to draw a scatter plot. It takes data_points and parameter as arguments  //
	////////////////////////////////////////////////////////////////////////////////////////////////

	function drawScatterPlot(data_points, parameter) {
		var chart = dc.seriesChart("#graph_display");
		

		// Time format coming in from API assigned to variable "z" is 2017-11-21 19:24:31.093000+00:00
		var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S.%L000+00:00").parse;

		data_points.forEach(function (d) {
			d.z = parseDate(d.z);
		});

		var ndx = crossfilter(data_points);

		var runDimension = ndx.dimension(function(d) {
			// return d3.time.year(d.z);
			return d.z;
		});

		var runGroup = runDimension.group().reduceSum(function(d) {
			return d.y;
		});

		var min_x = runDimension.bottom(1)[0];
		var max_x = runDimension.top(1)[0];

		var symbolScale = d3.scale.ordinal().range(d3.svg.symbolTypes);
		var symbolAccessor = function(d) {
			return symbolScale(d.key[0]);
		};

		var subChart = function(c) {
			return dc.scatterPlot(c).symbol(symbolAccessor).symbolSize(8).highlightedSize(10).elasticY(true)
		};

		chart
		.width(graph_width)
		.height(400)
		.chart(subChart)
		// .x(d3.scale.linear().domain([min_x.x, max_x.x]))
		.x(d3.time.scale().domain([min_x.z, max_x.z]))
		.brushOn(false)
		.yAxisLabel(parameter)
		.xAxisLabel("Time")
		.clipPadding(10)
		.elasticY(true)
		.dimension(runDimension)
		.group(runGroup)
		.mouseZoomable(true)
		.seriesAccessor(function(d) {
			return "Run";
		})
		.keyAccessor(function(d) {
			return +d.key;
		})
		.valueAccessor(function(d) {
			return +d.value;
		})
		.title(function (d) {
            return "Run start time: " + d.key + "\n" + "Mean value: " + d.value;
        })
		.legend(dc.legend().x(100).y(20).itemHeight(13).gap(5).horizontal(1).legendWidth(140).itemWidth(70));

		chart.yAxis().tickFormat(function(d) {
			return d3.format(',.2f')(d);
		});

		chart.margins().left += 40;

		dc.renderAll();

		var resizeTimer;		
		$(window).on('resize', function(e) {
	
			clearTimeout(resizeTimer);
			resizeTimer = setTimeout(function() {
				graph_width = target_element.style.width = getInnerWidth(target_element);	
				chart
				.width(graph_width)
				dc.renderAll();
			}, 450);
		});
	};

	///////////////////////////////////////////////////////////////////////////////////////////////
	// Define a function to draw a line chart. It takes graph_data and parameter as arguments    //
	///////////////////////////////////////////////////////////////////////////////////////////////

	function drawLineChart(line_data, parameter) {
		var chart = dc.lineChart("#graph_display");
		var ndx = crossfilter(line_data);
		var y_values = [];
		for(var i=0; i < line_data.length; i++)
		{
			y_values.push(line_data[i].y);
		}
		var y_max = Math.max.apply(null, y_values);
		var y_min = Math.min.apply(null, y_values);

		var runDimension = ndx.dimension(function(d) {
			return d.x;
		});

		var runGroup = runDimension.group().reduceSum(function(d) {
			return d.y;
		});

		var min_x = runDimension.bottom(1)[0];
		var max_x = runDimension.top(1)[0];

		console.log(y_max);
		console.log(y_min);


		// var min_y = min_x.y * 0.97;
		// var max_y = max_x.y * 1.03;

		chart
		.width(graph_width)
		.height(graph_width/2.5)
		.x(d3.scale.linear().domain([min_x.x, max_x.x]))
		.y(d3.scale.linear().domain([y_min, y_max]))
		.yAxisLabel(parameter)
		.xAxisLabel("Time")
		.clipPadding(10)
		.xAxisPadding(20)
		.yAxisPadding('5%')
		.renderLabel(true)
        .label(function (p) {
            return p.key;
		})
		.renderTitle(true)
        .title(function (p) {
            return "Data point " + p.key + ('\n') + "Value: " + p.value
        })
		.elasticY(false)
		.renderDataPoints(true)
		.dimension(runDimension)
		.group(runGroup)
		.mouseZoomable(true)
		.brushOn(false);

		chart.yAxis().tickFormat(function(d) {
			return d3.format(',.4f')(d);
		});

		// chart.yAxis().ticks(15);

		chart.margins().left += 40;

		dc.renderAll();

		chart.on('filtered', function(chart) {
			var filters = chart.filters();
			if (filters.length) {
				var range = filters[0];
				console.log('Range:', range[0].toFixed(8), range[1].toFixed(8));
			} else console.log('No filters.');
		});

		var resizeTimer;		
		$(window).on('resize', function(e) {
	
			clearTimeout(resizeTimer);
			resizeTimer = setTimeout(function() {
				graph_width = target_element.style.width = getInnerWidth(target_element);	
				chart
				.width(graph_width)
				dc.redrawAll();						
			}, 250);	
		});
	};


	///////////////////////////////////////////////////////////////////////////////////////////////
	// Set an event listener for the home page graph raw data buttons. It constructs a URL 		 //
	// string from the sensor ID, parameter ID, run start time to run end time and orders it by	 //
	// time in ascending format. It then calls getLineChartData passing the unique URL string.	 //
	///////////////////////////////////////////////////////////////////////////////////////////////

	$("[id^='run-']").click(function() {
		var runThis = $(this);
		var parameterThis = $("[id^='parameter-'] option:selected");
		var runId = runThis.attr("data-run-id");
		var runStart = runThis.attr("data-run-start");
		var runEnd = runThis.attr("data-run-end");
		var runStartURI = encodeURIComponent(runStart);
		var runEndURI = encodeURIComponent(runEnd);
		var parameterId = parameterThis.attr("value");
		var sensorId = runThis.closest("td").prev().children().attr("data-sensor-id");
		// var url_string = "/expert/api/data/?sensor=" + sensorId + "&parameter=" + parameterId + "&time__gte=" + runStartURI + "&time__lte=" + runEndURI + "&ordering=time" + "&format=json"
		var url_string = "/expert/api/data/?parameter=" + parameterId + "&time__gte=" + runStartURI + "&time__lte=" + runEndURI + "&ordering=time" + "&format=json"
        getLineChartData(url_string);
	});
	
	///////////////////////////////////////////////////////////////////////////////////////////////
	// Define a function to retrieve data points, and parameter values for the line charts.		 //
	// It takes in a URL string as argument. It queries the API for AlgorithmRunResults data.	 //
	///////////////////////////////////////////////////////////////////////////////////////////////

	function getLineChartData(url_string) {
		$.getJSON(url_string, function(data) {
			if (data.length == 0) {
				var algorithm_run_id = algorithm_run_valid_id;
				var algorithm_run_id_str = algorithm_run_id.toString();
				var url_string = "/expert/api/algorithm-run-results/?algorithm_run=" + algorithm_run_id_str + "&format=json";
				getScatterPlotRunData(url_string)
				return;
			};
			var line_data = data;
			var graph_data = [];
			for (i = 0; i < line_data.length; i++) {
				// graph_data.push({"x":line_data[i].start_time, "y":line_data[i].value});
				if (line_data[0].parameter_value) {
					graph_data.push({
						"x": i,
						"y": line_data[i].parameter_value
					});
				} else {
					graph_data.push({
						"x": i,
						"y": line_data[i].value
					});
				};
			};
			drawLineChart(graph_data, line_data[0].parameter);
		});
		return;
	};

	// get runs
	function getRuns(url_string, algorithm_runs) {
		$.getJSON(url_string, function(data) {
			if (data.length > 0) {
				var results_url = "/expert/api/algorithm-run-results/?";
				var query_string = "runss=";
				var define_format = "&format=json";
				results_url = results_url + query_string;
				for (i = 0; i < data.length; i++) {
					results_url = results_url + data[i].id;
					if (i != (data.length - 1)) {
						results_url = results_url + ",";
					};
				};
				results_url = results_url + "&algorithm_runs=";
				for (i = 0; i < algorithm_runs.length; i++) {
					results_url = results_url + algorithm_runs[i];
					if (i != (algorithm_runs.length - 1)) {
						results_url = results_url + ",";
					};
				};
				if (parameter != -1) {
					var query_string = "&parameter="
					results_url = results_url + query_string + parameter;
				};
				results_url = results_url + define_format;
				getScatterPlotRunData(results_url);
			};
		});
	};

	// get algorithm_runs
	function getAlgorithmRuns(url_string) {
		$.getJSON(url_string, function(data) {
			if (data.length > 0) {
				if (mode == "time") {
					var results_url = "/expert/api/algorithm-time-results/?"
					var query_string = "algorithm_runs="
					var define_format = "&format=json"
					for (i = 0; i < data.length; i++) {
						results_url = results_url + query_string + data[i].id;
						if (i != (data.length - 1)) {
							results_url = results_url + ",";
						};
					};
					if (chamber != -1) {
						var query_string = "&chamber="
						results_url = results_url + query_string + chamber;
					};
					if (parameter != -1) {
						var query_string = "&parameter="
						results_url = results_url + query_string + parameter;
					};
					results_url = results_url + "&ordering=start_time" + define_format;
					getLineChartData(results_url);
				} else {
					algorithm_runs = []
					for (i = 0; i < data.length; i++) {
						algorithm_runs.push(data[i].id.toString());
					};
					var runs_url_string = "/expert/api/runs/?chamber=" + chamber + "&format=json";
					getRuns(runs_url_string, algorithm_runs);
				};
			};
		});
	};
});