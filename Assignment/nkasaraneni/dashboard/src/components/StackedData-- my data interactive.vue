<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
// A "extends" B means A inherits the properties and methods from B.
interface ScatterPoint extends Point{ 
    cluster: string;
}

export default {
    data() {
        // Here we define the local states of this component. If you think the component as a class, then these are like its private variables.
        return {
            data: [] as any,
            columns: [] as string[],  // column names
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 40, right: 20, top: 25, bottom: 60} as Margin,
        }
    },
    computed: {
        rerender() {
            return this.size;
        }
    },
    created() {
        // fetch the data via API request when we init this component. This will only get called once.
        // In axios anything we send back in the response are always bound to the "data" property.
        axios.get(`${server}/fetchStackedData`)
            .then(resp => { // check out the app.py in ./server/ to see the format
                this.data = resp.data.data; 
                this.columns = resp.data.columns;
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        onResize() {  // record the updated size of the target element
            let target = this.$refs.stackedContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: target.clientWidth - 50, height: target.clientHeight - 100 };
        },
        async initChart() {
            // append the svg object to the body of the page
            var svg = d3.select("#stacked-svg")
            .append("svg")
                .attr("width", this.size.width + this.margin.left + this.margin.right)
                .attr("height", this.size.height + this.margin.top + this.margin.bottom)
            .append("g")
                .attr("transform",
                    "translate(" + (this.margin.left + 10) + "," + (this.margin.top) + ")");

            // Parse the Data (Vue passes it in wrapped weirdly)
            var keys = JSON.parse(JSON.stringify(this.columns)).slice(1)
            let data: any[] = JSON.parse(JSON.stringify(this.data))
            console.log(data)

            //////////
            // AXIS //
            //////////

            // Add X axis
            var x = d3.scaleTime()
                .domain(d3.extent(data, function(d) { return new Date(d.datetime); }))
                .range([ 0, this.size.width - this.margin.right ]);
            var xAxis = svg.append("g")
                .attr("transform", "translate(0," + this.size.height + ")")
                .call(d3.axisBottom(x).ticks(5))

            // Add X axis label:
            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", this.size.width)
                .attr("y", this.size.height + 40)
                .attr("transform", "translate(0," + this.size.height - 20 + ")")
                .text("Time (year)");

            // Add Y axis label:
            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", 0)
                .attr("y", -20) 
                .attr("transform", "translate(" + 0 +"," + this.margin.top + ")")
                .text("# PM 2.5")
                .attr("text-anchor", "start")

            // Add Y axis
            var y = d3.scaleLinear()
                .domain([0, 200000])
                .range([ this.size.height, this.margin.top ]);
            svg.append("g")
                // .attr("transform", `translate(${this.size.width}, 0)`)
                .call(d3.axisLeft(y).ticks(5))

            
            // color palette
            var color = d3.scaleOrdinal()
                .domain(keys)
                .range(d3.schemeSet2);
                
            //stack the data?
            var stackedData = d3.stack()
                .keys(keys)
                (data)
                //console.log("This is the stack result: ", stackedData)

            //////////
            // BRUSHING AND CHART //
            //////////

            // Add a clipPath: everything out of this area won't be drawn.
            var clip = svg.append("defs").append("svg:clipPath")
                .attr("id", "clip")
                .append("svg:rect")
                .attr("width", this.size.width )
                .attr("height", this.size.height )
                .attr("x", 0)
                .attr("y", 0);

            // Add brushing
            var brush = d3.brushX()                 // Add the brush feature using the d3.brush function
                .extent( [ [0,0], [this.size.width,this.size.height] ] ) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
                .on("end", updateChart) // Each time the brush selection changes, trigger the 'updateChart' function

            // Create the scatter variable: where both the circles and the brush take place
            var areaChart = svg.append('g')
                .attr("clip-path", "url(#clip)")

            // Area generator
            var area = d3.area()
                .x(function(d) { return x(d.datetime); })
                .y0(function(d) { return y(d[0]); })
                .y1(function(d) { return y(d[1]); })

            // Show the areas
            areaChart
                .selectAll("mylayers")
                .data(stackedData)
                .enter()
                .append("path")
                .attr("class", function(d) { return "myArea " + d.key })
                .style("fill", function(d) { return color(d.key); })
                .attr("d", area)

            // Add the brushing
            areaChart
                .append("g")
                .attr("class", "brush")
                .call(brush);

            var idleTimeout
            function idled() { idleTimeout = null; }

            // A function that update the chart for given boundaries
            function updateChart(event,d) {
                extent = event.selection

                // If no selection, back to initial coordinate. Otherwise, update X axis domain
                if(!extent){
                if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
                x.domain(d3.extent(data, function(d) { return d.year; }))
                }else{
                x.domain([ x.invert(extent[0]), x.invert(extent[1]) ])
                areaChart.select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
                }

                // Update axis and area position
                xAxis.transition().duration(1000).call(d3.axisBottom(x).ticks(5))
                areaChart
                .selectAll("path")
                .transition().duration(1000)
                .attr("d", area)
            }

            //////////
            // HIGHLIGHT GROUP //
            //////////

            // What to do when one group is hovered
            const highlight = function(event,d){
            // reduce opacity of all groups
            d3.selectAll(".myArea").style("opacity", .1)
            // expect the one that is hovered
            d3.select("."+d).style("opacity", 1)
            }

            // And when it is not hovered anymore
            const noHighlight = function(event,d){
            d3.selectAll(".myArea").style("opacity", 1)
            }

            //////////
            // LEGEND //
            //////////

            // Add one dot in the legend for each name.
            var size = 20
            var legend_position = this.size.width + this.margin.right - 100
            svg.selectAll("myrect")
            .data(keys)
            .enter()
            .append("rect")
                .attr("x", legend_position)
                .attr("y", function(d,i){ return 30 + i*(size+5) - (size/3)}) // 100 is where the first dot appears. 25 is the distance between dots
                .attr("width", size)
                .attr("height", size)
                .style("fill", function(d){ return color(d)})
                .on("mouseover", highlight)
                .on("mouseleave", noHighlight)

            // Add one dot in the legend for each name.
            svg.selectAll("mylabels")
            .data(keys)
            .enter()
            .append("text")
                .attr("x", legend_position + size*1.2)
                .attr("y", function(d,i){ return 30 + i*(size+5) + (size/2)}) // 100 is where the first dot appears. 25 is the distance between dots
                .style("fill", function(d){ return color(d)})
                .text(function(d){ return d})
                .attr("text-anchor", "left")
                .style("alignment-baseline", "middle")
                .on("mouseover", highlight)
                .on("mouseleave", noHighlight)
        }
    },
    watch: {
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#stacked-svg').selectAll('*').remove()
                this.initChart()
            }
        }
    },
    // The following are general setup for resize events.
    mounted() {
        window.addEventListener('resize', debounce(this.onResize, 100)) 
        this.onResize()
    },
    beforeDestroy() {
       window.removeEventListener('resize', this.onResize)
    }
}
</script>

<!-- "ref" registers a reference to the HTML element so that we can access it via the reference in Vue.  -->
<!-- We use flex to arrange the layout-->
<template>
    <div id="my_dataviz" ref="stackedContainer" class="chart-container outer d-flex">
        <svg id="stacked-svg" width="100%" height="100%">
            <!-- all the visual elements we create in initChart() will be inserted here in DOM-->
        </svg>
    </div>
</template>

<style scoped>
.chart-container{
    height: 100%;
    flex-direction: row;
    flex-wrap: nowrap;
    width: 100%;
}

.outer{
    display: flex;
    justify-content: center;
    align-items:center;
    height: 500px;
}
</style>