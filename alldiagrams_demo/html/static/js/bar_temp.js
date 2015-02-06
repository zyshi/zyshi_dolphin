$( ".graphcontainer" ).append( "<div class='span6 autovisual' id='tagid'></div>" ); 
var target = "#tagid";

var dataInputFile = "/static/data/data3072.tsv";

var yLabel = "Average_household_size_(md-2000s)";
var xLabel = "Country";

var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 1020 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10, "%");

var chart = d3.select(target).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.tsv(dataInputFile, type, function(error, data) {
  x.domain(data.map(function(d) { return d.xinput; })); 
  y.domain([0, d3.max(data, function(d) { return d.yinput; })]);

  chart.append("text")      // text label for the x axis
        .attr("x", 500 )
        .attr("y", 480 )
        .style("text-anchor", "middle")
        .text(xLabel);

  chart.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  chart.append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text(yLabel); // y-label

  chart.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.xinput); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.yinput); })
      .attr("height", function(d) { return height - y(d.yinput); });

});

function type(d) {
  d.yinput = +d.yinput;
  return d;
}
