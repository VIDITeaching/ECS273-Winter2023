<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';

interface DataPoint{
    posX: number;
    posY: number;
}
interface DataReady{ 
    name: string;
    values : DataPoint[];
}

// Computed property: https://vuejs.org/guide/essentials/computed.html
// Lifecycle in vue.js: https://vuejs.org/guide/essentials/lifecycle.html#lifecycle-diagram

export default {
    data() {
        // Here we define the local states of this component. If you think the component as a class, then these are like its private variables.
        return {
            points: [] as DataReady[], // "as <Type>" is a TypeScript expression to indicate what data structures this variable is supposed to store.
            clusters: [] as string[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 30, right: 20, top: 20, bottom: 40} as Margin,
            gamma_value: 0.001 as number,
        }
    },
    computed: {
        // Re-render the chart whenever the window is resized or the data changes (and data is non-empty)
        rerender() {
            return (!isEmpty(this.points)) && this.size
        }
    },
    created() {
        // fetch the data via API request when we init this component. This will only get called once.
        // In axios anything we send back in the response are always bound to the "data" property.
        axios.get(`${server}/svmGamma/${this.gamma_value}`)
            .then(resp => { // check out the app.py in ./server/ to see the format
                this.points = resp.data.data; 
                this.clusters = resp.data.clusters;
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        buttonClick(){
            console.log(this.gamma_value);
             // fetch the data via API request when we init this component. This will only get called once.
        // In axios anything we send back in the response are always bound to the "data" property.
         axios.get(`${server}/svmGamma/${this.gamma_value}`)
            .then(resp => { // check out the app.py in ./server/ to see the format
                this.points = resp.data.data; 
                this.clusters = resp.data.clusters;
                return true;
            })
            .catch(error => console.log(error));
            d3.select('#scatter-svg2').selectAll('*').remove() // Clean all the elements in the chart
            this.initChart();

        },
        onResize() {  // record the updated size of the target element
            let target = this.$refs.scatterContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: target.clientWidth, height: target.clientHeight };
        },
        initChart() {
        
            // select the svg tag so that we can insert(render) elements, i.e., draw the chart, within it.
            let myWidth = 460 - this.margin.left - this.margin.right;
            let myHeight = 400 - this.margin.top - this.margin.bottom;

            var svg = d3.select("#scatter-svg2")
            .append("svg")
            .attr("width", myWidth + this.margin.left + this.margin.right)
            .attr("height", myHeight + this.margin.top + this.margin.bottom)
            .append("g")
            .attr("transform",
                    "translate(" + this.margin.left + "," + this.margin.top + ")");

            // A color scale: one color for each group
            var myColor = d3.scaleOrdinal()
                .domain(this.clusters)
                .range(d3.schemeSet2);

            // Add X axis --> it is a date format
            var x = d3.scaleLinear()
                .domain([0,9])
                .range([ 0, myWidth ]);
            svg.append("g")
                .attr("transform", "translate(0," + myHeight + ")")
                .call(d3.axisBottom(x));

            // Add Y axis
            var minY = 1;
            for(var tempPair of this.points){
                for(var tempValueDict of tempPair.values){
                    if(tempValueDict.posY<minY){
                        minY = tempValueDict.posY;
                    }
                }
            }
            var y = d3.scaleLinear()
                .domain( [minY,1.0])
                .range([ myHeight, 0 ]);
            svg.append("g")
                .call(d3.axisLeft(y));

            // Add the lines
            var line = d3.line()
                .x(function(d) { return x(+d.posX) })
                .y(function(d) { return y(+d.posY) })
            
            svg.selectAll("myLines")
                .data(this.points)
                .enter()
                .append("path")
                .attr("class", function(d){ return d.name })
                .attr("d", function(d){ return line(d.values) } )
                .attr("stroke", function(d){ return myColor(d.name) })
                .style("stroke-width", 4)
                .style("fill", "none")

            // Add the points
            svg
                // First we need to enter in a group
                .selectAll("myDots")
                .data(this.points)
                .enter()
                    .append('g')
                    .style("fill", function(d){ return myColor(d.name) })
                    .attr("class", function(d){ return d.name })
                // Second we need to enter in the 'values' part of this group
                .selectAll("myPoints")
                .data(function(d){ return d.values })
                .enter()
                .append("circle")
                    .attr("cx", function(d) { return x(d.posX) } )
                    .attr("cy", function(d) { return y(d.posY) } )
                    .attr("r", 5)
                    .attr("stroke", "white")

            
             // Add a legend (interactive)
             svg
                .selectAll("myLegend")
                .data(this.points)
                .enter()
                .append('g')
                .append("text")
                    .attr('x', function(d,i){ return 10+ (i)*70})
                    .attr('y', -10)
                    .text(function(d) { return d.name; })
                    .style("fill", function(d){ return myColor(d.name) })
                    .style("font-size", 15)
                


            // For transform, check out https://www.tutorialspoint.com/d3js/d3js_svg_transformation.htm, but essentially we are adjusting the positions of the selected elements.
            const title = svg.append('g')
                .append('text') // adding the text
                .attr('transform', `translate(${this.size.width / 2-80}, 366)`)
                .attr('dy', '0.5rem') // relative distance from the indicated coordinates.
                .style('text-anchor', 'middle')
                .style('font-weight', 'bold')
                .text('Classification report for SVM') // text content
        },
    },
    watch: {
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#scatter-svg2').selectAll('*').remove() // Clean all the elements in the chart
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
    <div class="chart-container d-flex" ref="scatterContainer">
        <table width="100%">
           <tr height="330">
            <td>
                <svg id="scatter-svg2" width="100%" height="400">
                    <!-- all the visual elements we create in initChart() will be inserted here in DOM-->
                </svg>
            </td>
           </tr>
           <tr>
            <td align="left" style="vertical-align: top;">
                <label :style="{ fontSize: '0.7rem'}"> Change Gamma Value(0.001~10):
                    <input type="text"  id="gamma_input" v-model="gamma_value" placeholder="Please input"/>
                </label>
                
                <button style="border:12ex" @click="buttonClick">Re-compute!</button>
            </td>
           </tr>
        </table>
        
    </div>
    
</template>

<style scoped>
.chart-container{
    height: 100%;
}
</style>