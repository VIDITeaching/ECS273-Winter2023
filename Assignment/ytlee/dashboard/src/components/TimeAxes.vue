<script setup lang=ts>
import * as vue from "vue"
import { Ref, ref } from "vue"
import * as d3 from "d3"

const props = defineProps({
    data: Object as () => Any[], 
    dateRange: Object as () => Any[],
    yMax: Number,
    target_year: Number,
})


const xScale = vue.computed(() => d3.scaleLinear().domain(props.dateRange).range([0, 400]))
vue.watch(() => props.target_year, () => {
    updateIndicator(xScale.value)
})

vue.onMounted(() => {
    init()
    updateAxis()
    updateIndicator(xScale.value)
})

function init() {
    const svg = d3.select('svg.timeaxes')
        .attr("viewBox", `0 0 400 400`)
        .attr("overflow", "visible")
    const axisGenerator = d3.axisBottom(xScale.value)
        .tickFormat(d => (+d % 5 == 0? d : ""))
        .ticks(props.dateRange[1] - props.dateRange[0])
    const dateAxis = svg.append("g")
    dateAxis.append("rect").attr("class", "shadow")
    dateAxis.call(axisGenerator);
    addAreaChart(props.data, xScale.value)
}

function addAreaChart(data, x) {
    console.log({data})
    // prepare data
    const keys = Object.keys(data[0]).filter(key => key != "year")
    const stackedData = d3.stack().keys(keys)(data)
    const svg = d3.select('svg.timeaxes')

    // Add Y axis
    // y axis label
    svg.append("text")
        .attr("text-anchor", "end")
        .attr("x", 0)
        .attr("y", -210 )
        .text("# of attacks")
        .attr("text-anchor", "start")

    const y = d3.scaleLinear()
        .domain([0, props.yMax])
        .range([ 0, -200 ]);
    svg.append("g")
        .call(d3.axisLeft(y).ticks(5))

    svg.selectAll("text").attr("font-size", "0.4rem")
    // Area generator
    const area = d3.area()
        .x(function(d) { return x(d.data.year); })
        .y0(function(d) { return y(d[0]); })
        .y1(function(d) { return y(d[1]); })

    // Show the areas
    var color = d3.scaleOrdinal()
        .domain(keys.sort())
        .range(d3.schemeSet2);
    // let color = d3.scaleOrdinal(d3.schemeCategory10)
    const areaChart = svg.append('g')
        .attr('class', 'area-chart')
            .selectAll("mylayers")
            .data(stackedData)
            .enter()
            .append("path")
            .attr("class", function(d) { return "myArea " + d.key })
            .style("fill", function(d) { console.log(d); return color(d.key); })
            .attr("d", area)
            .style("opacity", 0.8)

}

function updateAxis() {
    const svg = d3.select('svg.timeaxes')
    // time axes
    const dateAxis = d3.select('svg.timeaxes g')
    dateAxis.selectAll("g.tick line").attr("y2", (d, i) => (i%5 == 0)?8:5);
} 

function updateIndicator(xScale) {
    const svg = d3.select('svg.timeaxes')
    svg.selectAll("rect.indicator")
        .data([props.target_year])
        .join("rect")
        .attr("class", "indicator")
        .attr("x", d => xScale(d))
        .attr("y", -200)
        .attr("width", 1)
        .attr("height", 200)
        .attr("fill", "black")
}


</script>
<template>
    <div class=timeaxes-container> 
        <svg class=timeaxes></svg>
    </div>
</template>

<style scoped>
.timeaxes {
  width: 100%;
  height: 100%;
}
</style>