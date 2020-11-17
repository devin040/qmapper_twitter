import React, {Component} from 'react';
import * as d3 from "d3";
export default Vis;

function Vis(){

var width = 960;
var height = 600;
var svg = d3.select("svg");
svg.attr("width", width).attr("height", height);
    
 var label = function(d) {
    if (d.label === "author") {
        return "1";
      }else if (d.label === "tweet") {
        return "2";
      }else if (d.label === "context_entity") {
        return "3";
      }else{
        return "4";}
      }
    
var color = d3.scaleOrdinal(d3.schemeCategory20);
    
d3.json("d3test2.json", function(error, graph) {
  if error throw error;
 
  var lines = svg.append("g")
      .attr("class", "link")
      .selectAll("line")
      .data(graph.links)
      .enter().append("line");
      //.style("stroke-width", function(d) { return Math.sqrt(d.weight); });

  var circles = svg.append("g")
    .attr("class", "node")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
    .attr("r",5)
    .attr("fill", label);
      
 var linkForce = d3.forceLink()
   .links(graph.links)
   .id(function(d) {
       return d.id;
   });
    
  var simulation = d3.forceSimulation(graph.nodes)
    .force("link", linkForce)
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2))
    .on("tick", ticked);

  function ticked(){
    circles
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
    lines
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
  )}
 }
}
           
