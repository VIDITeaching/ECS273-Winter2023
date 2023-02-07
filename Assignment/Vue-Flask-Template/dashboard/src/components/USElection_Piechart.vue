<template>
 <div class="chart-container">
  <!-- <div id="tooltip-donut" style="position: absolute"> -->
  <h2 class="piechart-title">Trump and Biden Most Used Words</h2>
  <svg ref="pieChart" width="300" height="300"></svg>
  <div>
   <button class="button_trump" @click="changeToTrump">Trump</button>
   &nbsp
   <button class="button_biden" @click="changeToBiden">Biden</button>
  </div>
 </div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import { isEmpty, debounce } from "lodash";
import { server } from "../helper";
export default {
 data() {
  return {
   originalData: [],
   bidenData: [],
   //    currentData: [],
  };
 },
 mounted() {
  axios
   .get(`${server}/speechTrump`)
   .then((response) => {
    this.originalData = response.data;
    // this.currentData = this.originalData;
    this.drawPieChart(this.originalData);
   })
   .catch((error) => {
    console.error(error);
   });

  axios
   .get(`${server}/speechBiden`)
   .then((response) => {
    this.bidenData = response.data;
   })
   .catch((error) => {
    console.error(error);
   });
 },
 methods: {
  changeToTrump() {
   //    this.currentData = this.originalData;
   this.drawPieChart(this.originalData);
  },

  changeToBiden() {
   //    this.currentData = this.bidenData;
   this.drawPieChart(this.bidenData);
  },

  drawPieChart(piedata) {
   const svg = d3.select(this.$refs.pieChart);
   const width = +svg.attr("width");
   const height = +svg.attr("height");
   const radius = Math.min(width, height) / 2;

   var color = d3.scaleOrdinal()
    .range(["#4e79a7","#f28e2c","#e15759","#76b7b2","#59a14f","#edc949","#af7aa1","#ff9da7","#9c755f","#bab0ab"]);
   const pie = d3.pie().value((d) => d.count);
   const data = pie(piedata);
   var div = d3
    .select("body")
    .append("div")
    .attr("class", "tooltip-donut")
    .style("opacity", 0);

   var tooltip = d3
    .select("body")
    .append("div")
    .attr("class", "tooltip-donut")
    .style("position", "absolute")
    .style("z-index", "10")
    .style('font-size', '8px')
    .style("visibility", "hidden")
    // .style("background", "#333333")
    // .style("color", "white")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "1px")
    .style("border-radius", "5px")
    .style("padding", "10px")
    .text("a simple tooltip");

   const arc = d3
    .arc()
    .outerRadius(radius - 30)
    .innerRadius(0);

   const g = svg
    .append("g")
    .attr("transform", `translate(${width / 2}, ${height / 2})`);

   g.selectAll("path")
    .data(data)
    .enter()
    .append("path")
    .attr("d", arc)
    .style("fill", (d, i) => color(i))
    .on("mouseover", function (d, i) {
     tooltip.text(i.data.count+" times");
     tooltip.style("fill","white");
     return tooltip.style("visibility", "visible");
    })
    .on("mousemove", function () {
     var matrix = this.getScreenCTM().translate(
      +this.getAttribute("cx"),
      +this.getAttribute("cy")
     );
     return tooltip
      .style("top",  (window.pageYOffset + matrix.f - 30) + "px")
      .style("left", (window.pageXOffset + matrix.e + 15) + "px");
    })
    .on("mouseout", function () {
     return tooltip.style("visibility", "hidden");
    });
   // Mouseover
   // .on("mouseover", function (d, i) {
   //  d3.select(this).transition().duration("50").attr("opacity", ".85");
   //  div.transition().duration(50).style("opacity", 1);
   //  let words = i.data.count;
   //  var matrix = this.getScreenCTM()
   //     .translate(+ this.getAttribute("cx"), + this.getAttribute("cy"));
   //  div
   //   .html(words)
   //   .style("left", (window.pageXOffset + matrix.e + 15) + "px")
   //   .style("top", (window.pageYOffset + matrix.f - 30) + "px");
   // })
   // .on("mouseout", function (d, i) {
   //  d3.select(this).transition().duration("50").attr("opacity", "1");
   //  div.transition().duration("50").style("opacity", 0);
   // });
   g.selectAll("text")
    .data(data)
    .enter()
    .append("text")
    .text((d) => d.data.words)
    .attr(
     "transform",
     (d) =>
      `translate(${arc.centroid(d)}) rotate(${
       (((d.startAngle + d.endAngle) / 2) * 180) / Math.PI - 90
      })`
    )
    .style("text-anchor", "middle")
    .style("fill", "white")
    .style("font-size", "0.7em");
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
.piechart-title{
  color: #3d3d3d
}
.button_trump {
 background-color: #d82129; /* Trump Red */
 border: none;
 color: white;
 padding: 10px 20px;
 text-align: center;
 text-decoration: none;
 display: inline-block;
 font-size: 16px;
 border-radius: 8px;
}
.button_trump:hover {     
    /* background-color:yellow;     */
    opacity: 0.8
}
.button_biden {
 background-color: #113e88; /* Biden Blue */
 border: none;
 color: white;
 padding: 10px 20px;
 text-align: center;
 text-decoration: none;
 display: inline-block;
 font-size: 16px;
 border-radius: 8px;
}
.button_biden:hover {     
    opacity: 0.8    
}
.tooltip-donut {
 position: absolute;
 text-align: center;
 padding: 0.5rem;
 background: #ffffff;
 color: #313639;
 border: 1px solid #313639;
 border-radius: 8px;
 pointer-events: none;
 font-size: 1.3rem;
}
</style>
