import React, {Component} from 'react';
import * as d3 from "d3";
export default Vis;

function Vis(){

var width = 960,
    height = 500

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var force = d3.layout.force()
    .gravity(.05)
    .distance(100)
    .charge(-100)
    .size([width, height]);

d3.json("d3test2.json", function(json) {
  force
      .nodes(json.nodes)
      .links(json.links)
      .start();

  var link = svg.selectAll(".link")
      .data(json.links)
    .enter().append("line")
      .attr("class", "link")
      //.style("stroke-width", function(d) { return Math.sqrt(d.weight); });

  var node = svg.selectAll(".node")
      .data(json.nodes)
    .enter().append("g")
      .attr("class", "node")
      .call(force.drag);

  var label = function(d) {
    if (d.label === "author") {
        return "green";
      }else if (d.label === "tweet") {
        return "purple";
      }else if (d.label === "context_entity") {
        return "red";
      }else{
        return "blue";}
      }

  node.append("circle")
      .attr("r","5")
      .style("fill", label)
      .append("title")
      .text(function(d) { return d.text; });

  node.append("text")
      .attr("dx", 12)
      .attr("dy", ".35em")
      .text(function(d) { return d.name });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
});
}

           
