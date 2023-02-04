<template>
 <div>
  <div ref="chart"></div>
 </div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import { isEmpty, debounce } from "lodash";
import { server } from "../helper";

// let margin = { top: 0, right: 20, bottom: 30, left: 80 };
// let svgWidth = 720;
// let svgHeight = 300;
// let height = svgHeight - margin.top - margin.bottom;
// console.log(height);
// let width = svgWidth - margin.left - margin.right;
// let width = 720;
// let height = 300;

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
    .attr("width", 400)
    .attr("height", 300);

   const x = d3
    .scaleBand()
    .domain(data.map((d) => d.name))
    .range([0, 400])
    .padding(0.1);

   const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d.count)])
    .range([0, 400]);

   chart
    .selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", (d) => x(d.name))
    .attr("y", (d) => 500 - y(d.count))
    .attr("width", x.bandwidth)
    .attr("height", (d) => y(d.count))
    .attr("fill", "blue");

    chart
     .selectAll("text")
     .data(data)
     .enter()
     .append("text")
     .text((d) => d.name)
     .attr("x", (d) => x(d.name) + x.bandwidth() / 2)
     .attr("y", (d) => 500 - y(d.count) + 20)
     .attr("text-anchor", "middle")
     .style("fill", "white")
     .style("font-size", "10px");

      chart
    .append("text")
    .attr("x", 200)
    .attr("y", 20)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .text("Awesome Barchart");
  },
 },
};
</script>
