<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';
import { Bar, ComponentSize, Margin } from '../types';

export default {
    data() {
         return {
            bars: [] as Bar[],
            avg_areas: [] as number[],
            class_names: [] as string[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 20, right: 20, top: 20, bottom: 40} as Margin,
        }
    },
    computed: {
        // Re-render the chart whenever the window is resized or the data changes (and data is non-empty)
        rerender() {
            return (!isEmpty(this.bars)) && this.size
        }
    },
        created() {
        // fetch the data via API request when we init this component. This will only get called once.
        // In axios anything we send back in the response are always bound to the "data" property.
        axios.get(`${server}/fetchBarPlotData`)
            .then(resp => { // check out the app.py in ./server/ to see the format
                this.avg_areas = resp.data.avg_areas;
                this.class_names = resp.data.class_names;
                for (var i=0; i<this.avg_areas.length; i++) {
                    var bar = {
                        type: this.class_names[i],
                        value: this.avg_areas[i]
                    }
                    this.bars.push(bar);
                }
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        onResize() {  // record the updated size of the target element
            let target = this.$refs.barplotContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: target.clientWidth, height: target.clientHeight };
        },
        initChart() {
          // set the dimensions and margins of the graph
            var margin = {top: 30, right: 30, bottom: 70, left: 60},
                width = 460 - margin.left - margin.right,
                height = 400 - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select("#barplot-svg")
              .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform",
                      "translate(" + margin.left + "," + margin.top + ")");

            // X axis
            var x = d3.scaleBand()
              .range([0, width])
              .domain(this.class_names)
              .padding(0.3);
            svg.append("g")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(x))
              .selectAll("text")
                .attr("transform", "translate(-10,0)rotate(-45)")
                .style("text-anchor", "end");

            // Add Y axis
            var y = d3.scaleLinear()
              .domain([0, 200000])
              .range([height, 0]);
            svg.append("g")
              .call(d3.axisLeft(y));

            // Bars
            svg.selectAll("mybar")
              .data(this.bars)
              .enter()
              .append("rect")
                .attr("x", function(d) { return x(d.type); })
                .attr("y", function(d) { return y(d.value); })
                .attr("width", x.bandwidth())
                .attr("height", function(d) { return height - y(d.value); })
                .attr("fill", "#69b3a2")

            const title = svg.append('g')
                .append('text') // adding the text
                .attr('transform', `translate(190,0)`)
                .attr('dy', '0.5rem') // relative distance from the indicated coordinates.
                .style('text-anchor', 'middle')
                .style('font-weight', 'bold')
                .text('7 Types of Dry Bean\'s Average Area') // text content
        },
    },
    watch: {
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#barplot-svg').selectAll('*').remove() // Clean all the elements in the chart
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

<template>
    <div class="chart-container d-flex" ref="barplotContainer">
        <svg id="barplot-svg" width="100%" height="100%">
            <!-- all the visual elements we create in initChart() will be inserted here in DOM-->
        </svg>
    </div>
</template>

<style scoped>
.chart-container{
    height: 100%;
}
</style>