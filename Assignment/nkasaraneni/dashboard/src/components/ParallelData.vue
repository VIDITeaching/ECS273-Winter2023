<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';


export default {
    data() {
        // Here we define the local states of this component. If you think the component as a class, then these are like its private variables.
        return {
            data: [] as any,
            columns: [] as string[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 20, right: 20, top: 45, bottom: 20} as Margin,
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
        axios.get(`${server}/fetchParallelData`)
            .then(resp => { // check out the app.py in ./server/ to see the format
                this.data = resp.data.data; 
                this.columns = resp.data.columns;
                this.initChart();
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        onResize() {  // record the updated size of the target element
            let target = this.$refs.parallelContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: target.clientWidth - 80, height: target.clientHeight - 100 };
            this.initChart();
        },
        initChart() {
            // append the svg object to the body of the page
            var svg = d3.select("#parallel-svg")
            .append("svg")
                .attr("width", this.size.width + this.margin.left + this.margin.right)
                .attr("height", this.size.height + this.margin.top + this.margin.bottom)
            .append("g")
                .attr("transform",
                    "translate(" + (this.margin.left + 10) + "," + (this.margin.top) + ")");
            
            // make title
            svg.append("text")
                .attr("x", (this.size.width / 2))             
                .attr("y", - (this.margin.top / 2) - 7)
                .attr("text-anchor", "middle")  
                .style("font-size", "18px") 
                .text("Parallel Coordinates for Beijing Atmospheric Data");

            // Extract the list of dimensions we want to keep in the plot. Here I keep all except the column called Species
            let data : any[] = this.data
            let dimensions : any[] = this.columns

            // For each dimension, I build a linear scale. I store all in a y object
            const y = {}
            for (var i in dimensions) {
                let dim = dimensions[i]
                y[dim] = d3.scaleLinear()
                    .domain( d3.extent(data.map(d => d[dim])) )
                    .range([this.size.height - 25, 0])
            }

            // Build the X scale -> it find the best position for each Y axis
            var x = d3.scalePoint()
            .range([0, this.size.width])
            .padding(0.25)
            .domain(dimensions);

            // The path function take a row of the csv as input, and return x and y coordinates of the line to draw for this raw.
            function path(d) {
                return d3.line()(dimensions.map(function(p) { return [x(p), y[p](d[p])]; }));
            }

            // Draw the lines
            svg
            .selectAll("myPath")
            .data(data)
            .join("path")
            .attr("d",  path)
            .style("fill", "none")
            .style("stroke", "#69b3a2")
            .style("opacity", 0.5)

            // Draw the axis:
            svg.selectAll("myAxis")
            // For each dimension of the dataset I add a 'g' element:
            .data(dimensions).enter()
            .append("g")
            // I translate this element to its right position on the x axis
            .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
            // And I build the axis with the call function
            .each(function(d) { d3.select(this).call(d3.axisLeft().scale(y[d])); })
            // Add axis title
            .append("text")
                .style("text-anchor", "middle")
                .attr("y", -9)
                .text(function(d) { return d; })
                .style("fill", "black")

        }
    },
    watch: {
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#parallel-svg').selectAll('*').remove()
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
    <!-- Initialize a select button -->
    <select id="selectButton"></select>
    <!-- This is where the graph will be -->
    <div id="parallel_dataviz" ref="parallelContainer" class="chart-container outer d-flex">
        <svg id="parallel-svg" width="100%" height="100%">
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