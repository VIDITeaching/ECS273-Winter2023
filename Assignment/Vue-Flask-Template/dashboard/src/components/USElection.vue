<template>
 <div class="chart-container">
  <h2 class="barchart-title">Speaking Number of Time Count</h2>
  <div ref="chart"></div>
 </div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import { server } from "../helper";

let margin = { top: 20, right: 20, bottom: 30, left: 40 };
let width = 420 - margin.left - margin.right;
let height = 300 - margin.top - margin.bottom;

export default {
 mounted() {
  axios
   .get(`${server}/presidentName`)
   .then((response) => {
    this.renderChart(response.data);
   })
   .catch((error) => {
    console.error(error);
   });
 },
 methods: {
  renderChart(data) {
   console.log(data);
   const chart = d3
    .select(this.$refs.chart)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

   const x = d3
    .scaleBand()
    .domain(data.map((d) => d.name))
    .range([0, width])
    .padding(0.1);

   chart
    .append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x));

   const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d.count)])
    .range([height, 0]);

   var tooltip = d3
    .select("body")
    .append("div")
    .attr("class", "tooltip-donut")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    // .style("background", "#333333")
    // .style("color", "white")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "1px")
    .style("border-radius", "5px")
    .style("padding", "10px")
    .style('font-size', '10px')
    .text("a simple tooltip");

   chart.append("g").call(d3.axisLeft(y));

   chart
    .selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", (d) => x(d.name))
    .attr("y", (d) => y(d.count))
    .attr("width", x.bandwidth)
    .attr("height", (d) => height - y(d.count))
    .attr("fill", "#002868")
    .on("mouseover", function (d, i) {
     tooltip.text(i.name+" speaking count: " + i.count + " times");
     tooltip.style("fill", "white");
     d3.select(event.currentTarget).style("fill", "#215bb8")
     return tooltip.style("visibility", "visible");
    })
    .on("mousemove", function () {
     var matrix = this.getScreenCTM().translate(
      +this.getAttribute("cx"),
      +this.getAttribute("cy")
     );
     return tooltip
      .style("top", window.pageYOffset + matrix.f - 10 + "px")
      .style("left", window.pageXOffset + matrix.e + 15 + "px");
    })
    .on("mouseout", function () {
    d3.select(event.currentTarget).style("fill", "#002868")
     return tooltip.style("visibility", "hidden");
    });

   chart
    .selectAll("text")
    .data(data)
    .enter()
    .append("text")
    .text(function (d) {
     return d.count;
    })
    .attr("x", (d) => x(d.name) + x.bandwidth() / 2)
    .attr("y", (d) => y(d.count) - 10)
    .attr("text-anchor", "middle")
    .style("fill", "white")
    .style("font-size", "10px")
    .attr("dominant-baseline", "middle");

   //  chart
   //   .append("text")
   //   .attr("x", 200)
   //   .attr("y", 20)
   //   .attr("text-anchor", "middle")
   //   .style("font-size", "16px")
   //   .text("US Election Speaker Speaking Count");
  },
 },
};
</script>

<style scoped>
.chart-container{
    /* width: calc(100% - 5rem); */
    width: 450px; 
    height: 450px;
    /* align-items: center; */
    display:table-cell;
    vertical-align:middle;
    text-align:center;
    background: rgb(247, 247, 247);
    border-radius: 6px;
}
.barchart-title{
  color: #3d3d3d
}
</style>
