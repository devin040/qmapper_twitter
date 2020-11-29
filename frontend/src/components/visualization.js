import React, {useRef, useEffect} from 'react';
import * as d3 from "d3";


function Vis() {
    const d3Container = useRef(null);
    useEffect(
        () => {
var width = 960;
var height = 600;
var svg = d3.select(d3Container.current);
svg.attr("width", width).attr("height", height);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));

d3.json("d3test.json", function(error, graph) {
  if (error) throw error;

  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", 1);

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")

    var label = function(d) {
       if (d.label === "author") {
           return "red";
         }else if (d.label === "tweet") {
           return "blue";
         }else if (d.label === "context_entity") {
           return "green";
         }else{
           return "purple";}
         }

  var circles = node.append("circle")
      .attr("r", 5)
      .attr("fill", label);


  var lables = node.append("text")
      .text(function(d) {
        return d.name;
      })
      .attr('x', 6)
      .attr('y', 3);

  node.append("title")
      .text(function(d) { return d.id; });

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
        })
  }
});
},
[d3Container.current])

  return (
    <svg 
    className = "d3-component"
    width={960}
    height={600}
    ref = {d3Container}
    />
  );
}
export default Vis;
