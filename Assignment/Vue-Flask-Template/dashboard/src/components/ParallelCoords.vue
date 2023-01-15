
<template>
    <div class="viz-container d-flex justify-end">
    <div ref="parallelContainer" class="chart-container d-flex">
        <svg id="parallel-svg-interactions" width="100%" height="100%"></svg>
        
    </div>
</div>

</template>

<!-- 
<template>
    <div class="viz-container d-flex justify-end">
        <div class="chart-container d-flex" ref="scatterContainer">
            <svg id="scatter-svg-interactions" width="100%" height="100%">
            </svg>
        </div>
        <div id="scatter-control-container" class="d-flex">
            <div class="d-flex mb-4">
                <label :style="{ fontSize: '0.7rem'}"> Select DR method:
                    <select class="method-select" v-model="store.selectedMethod">
                        <option v-for="method in store.methods" :value="method" 
                            :selected="(method === store.selectedMethod)? true : false">{{method}}</option>
                    </select>
                </label>
            </div>
            <svg id="scatter-legend-svg-interactions" width="100%" height="80%">
            </svg>
        </div>

    </div>
</template> -->

<script allowJS lang="ts">
import * as d3 from 'd3';

import axios from 'axios';

import { Point, ComponentSize, Margin } from '../types';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';
// For importing a store. See how it's set up in ./dashboard/stores/ and ./dashboard/main.ts
import { mapState, storeToRefs } from 'pinia'; 
import { useRentStore } from '../stores/rentStore';
export default {
    setup() { // Composition API syntax
        const store = useRentStore()
        // Alternative expression from computed
        const { resize } = storeToRefs(store);
        return {
            store, // Return store as the local state, but when you update the property value, the store is also updated.
            resize,
        }
    },
    computed: {
        ...mapState(useRentStore, ['selectedMethod']) // Traditional way to map the store state to the local state
    },

    created() {
        this.store.fetchRent(this.selectedMethod);
    },

    methods: {

        onResize() {
            let target = this.$refs.parallelContainer as HTMLElement
            if (target === undefined || target === null) return;
            this.store.size = { width: target.clientWidth, height: target.clientHeight };
        },
        async initChart() {
            // set the dimensions and margins of the graph
            // const margin = { top: 30, right: 10, bottom: 10, left: 0 },
            //     width = 500 - margin.left - margin.right,
            //     height = 400 - margin.top - margin.bottom;

            let chartContainer = d3.select('#parallel-svg-interactions')
            // append the svg object to the body of the page
            const svg = chartContainer
                .append("g")
                
                .attr("ref", 'idk')
                .attr('width', '100%')
                .attr('height', '100%')
                // .attr("width", this.store.size.width + this.store.margin.left + this.store.margin.right)
                // .attr("height", this.store.size.height + this.store.margin.top + this.store.margin.bottom)
                
                .attr("transform",
                    `translate(${this.store.margin.left},${this.store.margin.top})`);



            // console.log('data iris: ', data)
            // Extract the list of dimensions we want to keep in the plot. Here I keep all except the column called Species
            // let dimensions = Object.keys(data[0]).filter(function (d) { return d != "Species" })
            // console.log('dimensions: ', dimensions)


            // let data = await d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/iris.csv").then(function (data) {
            //     // Extract the list of dimensions we want to keep in the plot. Here I keep all except the column called Species
            //     // let dimensions = Object.keys(data[0]).filter(function(d) { return d != "Species" })
            //     // console.log('dimensions: ', dimensions)
            //     return data
            // })

            let data = this.store.rent;
            console.log('this.store.rent[0]: ', this.store.rent[1])
            let dimensions = Object.keys(this.store.rent[0]).filter(function (d) { return d == 'baths' || d == 'beds' || d == 'price' || d == 'sqft' })


            console.log('dimensions2: ', dimensions)
            // For each dimension, I build a linear scale. I store all in a y object
            const y: { [key: string]: d3.ScaleLinear<number, number> } = {};
            for (const name of dimensions) {
                console.log('name: ', name)
                if(data.length > 0 && data[0][name]) {
                    y[name] = d3.scaleLinear()
                        .domain(d3.extent(data, (d) => +d[name]))
                        .range([this.store.size.height - this.store.margin.bottom, this.store.margin.top]);
                }
            }

            // Build the X scale -> it find the best position for each Y axis
            let x = d3.scalePoint()
                .range([0, this.store.size.width - this.store.margin.right])
                .padding(.1)
                .domain(dimensions);

                console.log('x: ', x)
            // The path function take a row of the csv as input, and return x and y coordinates of the line to draw for this raw.
            function path(d: { [x: string]: d3.NumberValue; }) {
                return d3.line()(dimensions.map(function (p) { return [x(p), y[p](d[p])]; }));
            }

            const color = d3.scaleOrdinal()
                .domain(["setosa", "versicolor", "virginica" ])
                .range([ "#440154ff", "#21908dff", "#fde725ff"])

            // Highlight the specie that is hovered
            const highlight = function(event: any, d: { city: any; }){

            // first every group turns grey
            d3.selectAll(".line")
            .transition().duration(200)
            .style("stroke", "lightgrey")
            .style("opacity", "0.2")
            // Second the hovered specie takes its color
            d3.selectAll("." + d.city)
            .transition().duration(200)
            .style("stroke", (d: any) => `${color(d.city)}`)
            .style("opacity", "1")
            }

            // Unhighlight
            const doNotHighlight = function(event: any, d: any){
            d3.selectAll(".line")
            .transition().duration(200).delay(1000)
            .style("stroke", (d: any) => `${color(d.city)}`)
            .style("opacity", "1")
            } 

            // Draw the lines
            svg
                .selectAll("myPath")
                .data(data)
                .join("path")
                    .attr("class", (d: any) => `line ${d.city}`)
                    .attr("d", path)
                    .style("fill", "none")
                    .style("stroke", (d: any) => `${color(d.city)}` )
                    // .style("stroke", "#69b3a2")
                    .style("opacity", 0.5)
                    .on("mouseover", highlight)
                    .on("mouseleave", doNotHighlight )

            // Draw the axis:
            svg.selectAll("myAxis")
                // For each dimension of the dataset I add a 'g' element:
                .data(dimensions).enter()
                .append("g")
                // I translate this element to its right position on the x axis
                .attr("transform", function (d) { return "translate(" + x(d) + ")"; })
                // And I build the axis with the call function
                .each(function (d) { d3.select(this).call(d3.axisLeft().scale(y[d])); })
                // Add axis title
                .append("text")
                .style("text-anchor", "middle")
                .attr("y", -9)
                .text(function (d) { return d; })
                .style("fill", "black")

        },

        rerender() {

            d3.select('#parallel-svg-interactions').selectAll('*').remove() // Clean all the elements in the chart
            // d3.select('#my_dataviz').selectAll('*').remove()
            this.initChart()
        }
    },
    watch: { // updated because a legend is added.
        
        resize(newSize) { // when window resizes
            if ((newSize.width !== 0) && (newSize.height !== 0)) {
                this.rerender()
            }
        },
        'store.rent'(data) { // when data changes
            if (!isEmpty(data)) {
                this.rerender()
            }
        },
        
        selectedMethod(newMethod) { // function triggered when a different method is selected via dropdown menu
            this.store.fetchRent(newMethod)
        },
    },
    mounted() {
        window.addEventListener('resize', debounce(this.onResize, 100))
        this.onResize()
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    }
}
</script>


<style scoped>
.viz-container{
    height:100%;
    width: 100%; 
    flex-direction: row;
    flex-wrap: nowrap;
}
.chart-container{
    height: 100%;
    flex-direction: row;
    flex-wrap: nowrap;
    width: 100%; 
    /* calc(100% - 6rem); */
}
#parallel{
    width: 6rem;
    flex-direction: column;
}

.method-select{
    outline: solid;
    outline-width: 1px;
    outline-color: lightgray;
    border-radius: 2px;
    width: 100%;
    padding: 2px 5px;
}
</style>