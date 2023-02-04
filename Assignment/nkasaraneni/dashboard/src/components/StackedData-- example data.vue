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
            points: [] as ScatterPoint[], // "as <Type>" is a TypeScript expression to indicate what data structures this variable is supposed to store.
            clusters: [] as string[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 20, right: 20, top: 20, bottom: 40} as Margin,
        }
    },
    computed: {
        rerender() {
            return this.size;
        }
    },
    methods: {
        onResize() {  // record the updated size of the target element
            let target = this.$refs.stackedContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: target.clientWidth, height: target.clientHeight };
        },
        async initChart() {
            console.log('init chart runs')
            // append the svg object to the body of the page
            var svg = d3.select("#stacked-svg")
            .append("svg")
                .attr("width", this.size.width + this.margin.left + this.margin.right)
                .attr("height", this.size.height + this.margin.top + this.margin.bottom)
            .append("g")
                .attr("transform",
                    "translate(" + this.margin.left + "," + this.margin.top + ")");

            // Parse the Data
            let data = await d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/5_OneCatSevNumOrdered_wide.csv")
            console.log(data)
            // List of groups = header of the csv files
            var keys = data.columns.slice(1)

            // Add X axis
            var x = d3.scaleLinear()
                .domain(d3.extent(data, function(d) { return d.year; }))
                .range([ 0, this.size.width ]);
            svg.append("g")
                .attr("transform", "translate(0," + this.size.height + ")")
                .call(d3.axisBottom(x).ticks(5));

            // Add Y axis
            var y = d3.scaleLinear()
                .domain([0, 200000])
                .range([ this.size.height, 0 ]);
            svg.append("g")
                .call(d3.axisLeft(y));

            // color palette
            var color = d3.scaleOrdinal()
                .domain(keys)
                .range(['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf'])

            //stack the data?
            var stackedData = d3.stack()
                .keys(keys)
                (data)
                //console.log("This is the stack result: ", stackedData)

            // Show the areas
            svg
                .selectAll("mylayers")
                .data(stackedData)
                .enter()
                .append("path")
                .style("fill", function(d) { console.log(d.key) ; return color(d.key); })
                .attr("d", d3.area()
                    .x(function(d, i) { return x(d.data.year); })
                    .y0(function(d) { return y(d[0]); })
                    .y1(function(d) { return y(d[1]); })
                )
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
    <h3>testing</h3>
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