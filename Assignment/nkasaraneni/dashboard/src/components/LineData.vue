<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';

// NOTES TO SELF:
// d3.extent to find min and max of hours array
// array.map for quick selection 
export default {
    data() {
        // Here we define the local states of this component. If you think the component as a class, then these are like its private variables.
        return {
            data: [] as any,
            columns: [] as string[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 55, right: 40, top: 20, bottom: 40} as Margin,
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
        axios.get(`${server}/fetchLineData`)
            .then(resp => { // check out the app.py in ./server/ to see the format
                this.data = resp.data.data; 
                this.columns = resp.data.columns;
                d3.select('#selectButton').selectAll('*').remove();
                this.initChart();
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        onResize() {  // record the updated size of the target element
            let target = this.$refs.lineContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: target.clientWidth - 80, height: target.clientHeight - 100 };
        },
        initChart() {
            // append the svg object to the body of the page
            var svg = d3.select("#line-svg")
            .append("svg")
                .attr("width", this.size.width + this.margin.left + this.margin.right)
                .attr("height", this.size.height + this.margin.top + this.margin.bottom)
            .append("g")
                .attr("transform",
                    "translate(" + (this.margin.left + 10) + "," + (this.margin.top) + ")");

            // make title
            svg.append("text")
                .attr("x", (this.size.width / 2))             
                .attr("y", - (this.margin.top / 2) + 10)
                .attr("text-anchor", "middle")  
                .style("font-size", "18px") 
                .text("PM 2.5 Change Over Time (Filter by Station)");

            //Read the data
            let data = this.data
            console.log("length of line data" + data.length)

            // List of groups (here I have one group per column)
            var cities = ['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng',
                        'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan','Wanliu','Wanshouxigong']
            
            // add the options to the button
            d3.select("#selectButton")
            .selectAll('myOptions')
                .data(cities)
            .enter()
                .append('option')
            .text(function (d) { return d; }) // text showed in the menu
            .attr("value", function (d) { return d; }) // corresponding value returned by the button

            // Add X axis --> it is a date format
            const xMax : any = d3.max(data.map(d => d.hour)) - d3.min(data.map(d => d.hour))
            console.log("xMax: " + xMax)
            var x = d3.scaleLinear()
            .domain([0, xMax])
            .range([ 0, this.size.width ]);
            svg.append("g")
            .attr("transform", "translate(0," + this.size.height + ")")
            .call(d3.axisBottom(x));
            // add X axis label
            svg.append("text")
                .attr("class", "x label")
                .attr("text-anchor", "end")
                .attr("x", this.size.width)
                .attr("y", this.size.height + 35)
                .text("hour in year");
               
            // Add Y axis
            var y = d3.scaleLinear()
            .domain( [2,450])
            .range([ this.size.height, 0 ]);
            svg.append("g")
            .call(d3.axisLeft(y));
            // Add Y axis label:
            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", -this.size.height/1.75)
                .attr("y", -this.margin.left) 
                .attr("dy", ".75em")
                .attr("transform", "rotate(-90)")
                // .attr("transform", "translate(" + 0 +"," + this.margin.top + ")")
                .text("PM 2.5 Level")
                .attr("text-anchor", "start")


            // Initialize line with group a
            var line = svg
            .append('g')
            .append("path")
                .datum(data)
                .attr("d", d3.line()
                    .x(function(d) { return x(+d.hour - d3.min(data.map(d => d.hour))) })
                    .y(function(d) { return y(+d.Aotizhongxin) })
                )
                .attr("stroke", "black")
                .style("stroke-width", 4)
                .style("fill", "none")

            // Initialize dots with group a
            var dot = svg
            .selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
                .attr("cx", function(d) { return x(+d.hour - d3.min(data.map(d => d.hour))) })
                .attr("cy", function(d) { return y(+d.Aotizhongxin) })
                .attr("r", 7)
                .style("fill", "#69b3a2")


            // A function that update the chart
            function update(selectedGroup) {

            // Create new data with the selection?
            var dataFilter = data.map(function(d){return {hour: d.hour, value:d[selectedGroup]} })

            // Give these new data to update line
            line
                .datum(dataFilter)
                .transition()
                .duration(1000)
                .attr("d", d3.line()
                    .x(function(d) { return x(+d.hour - d3.min(data.map(d => d.hour))) })
                    .y(function(d) { return y(+d.value) })
                )
            dot
                .data(dataFilter)
                .transition()
                .duration(1000)
                .attr("cx", function(d) { return x(+d.hour - d3.min(data.map(d => d.hour))) })
                .attr("cy", function(d) { return y(+d.value) })
            }

            // When the button is changed, run the updateChart function
            d3.select("#selectButton").on("change", function(d) {
                // recover the option that has been chosen
                var selectedOption = d3.select(this).property("value")
                // run the updateChart function with this selected option
                update(selectedOption)
            })


        }
    },
    watch: {
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#line-svg').selectAll('*').remove()
                d3.select('#selectButton').selectAll('*').remove()
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
    <div id="line_dataviz" ref="lineContainer" class="chart-container outer d-flex">
        <svg id="line-svg" width="100%" height="100%">
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