<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce, range } from 'lodash';
import { server } from '../helper';

import { Point, PointMat, ComponentSize, Margin } from '../types';
import { fcumsum } from "d3";
// A "extends" B means A inherits the properties and methods from B.
interface ScatterPoint extends Point{ 
    cluster: string;
}

interface HeatMapPoint extends PointMat{ 
    corr: number;
}

// Computed property: https://vuejs.org/guide/essentials/computed.html
// Lifecycle in vue.js: https://vuejs.org/guide/essentials/lifecycle.html#lifecycle-diagram

export default {
    data() {
        // Here we define the local states of this component. If you think the component as a class, then these are like its private variables.
        return {
            points: [] as HeatMapPoint[], // "as <Type>" is a TypeScript expression to indicate what data structures this variable is supposed to store.
            clusters: [] as number[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 20, right: 20, top: 20, bottom: 80} as Margin,
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
        axios.get(`${server}/fetchCorrMat`)
            .then(resp => { // check out the app.py in ./server/ to see the format
                this.points = resp.data.data; 
                this.clusters = resp.data.clusters;
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        onResize() {  // record the updated size of the target element
            let target = this.$refs.scatterContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: target.clientWidth, height: target.clientHeight };
        },
        initChart() {
            // set the dimensions and margins of the graph
            const margin = { top: 80, 
                                right: this.margin.right, 
                                bottom: this.margin.bottom, 
                                left: this.margin.left + 60},
                                width = 450 - margin.left - margin.right,
                                height = 450 - margin.top - margin.bottom;
                                //width = this.size.width - this.margin.left,
                                //height = this.size.height - 5*this.margin.bottom;

            // append the svg object to the body of the page
            const svg = d3.select('#scatter-bean2-svg')
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);


            // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
            const myGroups = Array.from(new Set(this.points.map(d => d.posX))) as string[]
            const myVars = Array.from(new Set(this.points.map(d => d.posY))) as string[]

            // Build X scales and axis:
            const x = d3.scaleBand()
                .range([0, width])
                .domain(myGroups)
                .padding(0.05);
            svg.append("g")
                .style("font-size", 10)
                .attr("transform", `translate(0, ${height})`)
                .call(d3.axisBottom(x).tickSize(0))
                .selectAll("text")
                .attr("transform", "translate(-10,40)rotate(-90)")
                .select(".domain").remove()

            // Build Y scales and axis:
            const y = d3.scaleBand()
                .range([height, 0])
                .domain(myVars)
                .padding(0.05);
            svg.append("g")
                .style("font-size", 10)
                .call(d3.axisLeft(y).tickSize(0))
                .select(".domain").remove()
            

            // Build color scale
            const myColor = d3.scaleSequential()
                .interpolator(d3.interpolateInferno)
                .domain([-1, 1])

            // create a tooltip
            var div = d3.select("body").append("div")
                .attr("class", "tooltip")
                .style("opacity", 0.5);


            // Three function that change the tooltip when user hover / move / leave a cell
            const mouseover = function (this: any, event: any, d: any) {
                div
                    .style("opacity", 0.5),
                    d3.select(this)
                        .style("stroke", "black")
                        .style("opacity", 1)
            }
            // function mousmove_fcn (this:any, event:MouseEvent, d:HeatMapPoint) {
            //     tooltip
            //         .html("The exact value of<br>this cell is: " + d.corr)
            //         .style("left", (event.x) / 2 + "px")
            //         .style("top", (event.y) / 2 + "px")
            //     console.log(this)
            // }
            // const mousemove = mousmove_fcn.bind(d3)

            // var div = d3.select("#scatter-bean2-svg").append("div")
            //     .attr("class", "tooltip")
            //     .style("opacity", 0);

            const mousemove = function (this:any, event:MouseEvent, d:HeatMapPoint) {
                div.transition()
                    .style("opacity", 1.0);
                div
                .style("left", (event.pageX) + "px")
                .style("top", (event.pageY - 25) + "px")
                .html("<span style='color:white'>" + d.corr.toFixed(2) + "</span><br>")
                
                // .style("left", (event.x) + "px")
                // .style("top", (event.y-20) + "px")
                
                //.html("The exact value of<br>this cell is: " + d.corr)
            }
    //                 div.transition()
    //     .duration(100)
    //     .style("opacity", 0.8);
    //   div.html("<span class='year'>" + d.year + " - " + month[d.month - 1] + "</span><br>" +
    //       "<span class='temperature'>" + (Math.floor((d.variance + baseTemp) * 1000) / 1000) + " &#8451" + "</span><br>" +
    //       "<span class='variance'>" + d.variance + " &#8451" + "</span>")
    //     .style("left", (d3.event.pageX - ($('.tooltip').width()/2)) + "px")
    //     .style("top", (d3.event.pageY - 75) + "px");
            
            
            const mouseleave = function (this: any, event: any, d: any) {
                div
                    .style("opacity", 0)
                d3.select(this)
                    .style("stroke", "none")
                    .style("opacity", 0.8)
            }

            // add the squares
            svg.selectAll()
                .data(this.points, function (d: any) { return d.posX + ':' + d.posY; })
                .join("rect")
                .attr("x", d => x(d.posX) as number)
                .attr("y", d => y(d.posY) as number)
                .attr("rx", 4)
                .attr("ry", 4)
                .attr("width", x.bandwidth())
                .attr("height", y.bandwidth())
                .style("fill", function (d) { return myColor(d.corr) })
                .style("stroke-width", 4)
                .style("stroke", "none")
                .style("opacity", 0.8)
                .on("mousemove", mousemove)
                .on("mouseleave", mouseleave)
                .on("mouseover", mouseover) 
                
                //.on("mousemove", mousemove)

            // Add title to graph
            svg.append("text")
                .attr("x", 0)
                .attr("y", -50)
                .attr("text-anchor", "left")
                .style("font-size", "15px")
                .text("Correlation matrix heat map of bean traits");

            // Add subtitle to graph
            svg.append("text")
                .attr("x", 0)
                .attr("y", -20)
                .attr("text-anchor", "left")
                .style("font-size", "10px")
                .style("fill", "grey")
                .style("max-width", 400)
                .text("The brighter the color, the higher the correlation.");
                          


            /////////////////////////////////////////////
            // select the svg tag so that we can insert(render) elements, i.e., draw the chart, within it.
            // let chartContainer = d3.select('#scatter-bean2-svg')

            // // we need compute the [min, max] from the data values of the attributes that will be used to represent x- and y-axis.
            // let xExtents = d3.extent(this.points.map((d: ScatterPoint) => d.posX as number)) as [number, number]
            // let yExtents = d3.extent(this.points.map((d: ScatterPoint) => d.posY as number)) as [number, number]

            // // We need a way to map our data to where it should be rendered within the svg (in pixels) based on the data value, 
            // //      so the extents above help us define the limits.
            // // Scales are just like mapping functions y = f(x), where x refers to domain, y refers to range in this case.
            // // We have the margin here just to leave some space
            // // In viewport (our screen), the leftmost side always refer to 0 in the horizontal coordinates in pixels (x). 
            // let xScale = d3.scaleLinear()
            //     .range([this.margin.left, this.size.width - this.margin.right]) // left side to the right side on the screen
            //     .domain(xExtents)

            // // In viewport (our screen), the topmost side always refer to 0 in the vertical coordinates in pixels (y). 
            // let yScale = d3.scaleLinear()
            //     .range([this.size.height - this.margin.bottom, this.margin.top]) //bottom side to the top side on the screen
            //     .domain(yExtents)
            // // There are other scales such as scaleOrdinal and scaleBand, 
            //     // whichever is appropriate depends on the data types and the kind of visualizations you're creating.

            // /*
            // // This following part visualizes the axes. We did not do it because the x- and y- axis in DR projections usually mean nothing for interpretation.
            // // Check out https://observablehq.com/@d3/margin-convention?collection=@d3/d3-axis
            // // Note that for axis labels, this is just a demostration, their positions are not perfect.
            // const xAxis = chartContainer.append('g')
            //     .attr('transform', `translate(0, ${this.size.height - this.margin.bottom})`)
            //     .call(d3.axisBottom(xScale))

            // const yAxis = chartContainer.append('g')
            //     .attr('transform', `translate(${this.margin.left}, 0)`)
            //     .call(d3.axisLeft(yScale))

            // const yLabel = chartContainer.append('g')
            //     .attr('transform', `translate(${this.margin.left}, ${this.size.height / 2 + this.margin.top}) rotate(-90)`)
            //     .append('text')
            //     .text('PC2')

            // const xLabel = chartContainer.append('g')
            //     .attr('transform', `translate(${this.size.width / 2}, ${this.size.height - this.margin.top})`)
            //     .append('text')
            //     .text('PC1')
            // */

            // // Similar to above but now we are creating the color scale with scaleOrdinal.
            // let clusters: string[] = this.clusters.map((cluster: string, idx: number) => String(idx))
            // let colorScale = d3.scaleOrdinal().domain(clusters).range(d3.schemeTableau10) // d3.schemeTableau10: string[]

            // // "g" is group element that does nothing but helps avoid DOM looking like a mess
            // // We iterate through each <ScatterPoint> element in the array, create a circle for each and indicate the coordinates, the circle size, the color, and the opacity.
            // const points = chartContainer.append('g')
            //     .selectAll('circle') //adding circles
            //     .data<ScatterPoint>(this.points) // TypeScript expression
            //     .join('circle')
            //     .attr('cx', (d: ScatterPoint) => xScale(d.posX))
            //     .attr('cy', (d: ScatterPoint) => yScale(d.posY))
            //     .attr('r', 5)
            //     .style('fill', (d: ScatterPoint) => colorScale(String(d.cluster)) as string)
            //     .style('opacity', .7)

            // // For transform, check out https://www.tutorialspoint.com/d3js/d3js_svg_transformation.htm, but essentially we are adjusting the positions of the selected elements.
            // const title = chartContainer.append('g')
            //     .append('text') // adding the text
            //     .attr('transform', `translate(${this.size.width / 2}, ${this.size.height - this.margin.top})`)
            //     .attr('dy', '0.5rem') // relative distance from the indicated coordinates.
            //     .style('text-anchor', 'middle')
            //     .style('font-weight', 'bold')
            //     .text('VIS2') // text content

            ///////////////////////////////////////////

        },

        initLegend() {
            let legendContainer = d3.select('#heatmap-legend-svg')

            //let clusterLabels: string[] = this.store.clusters.map((cluster: string, idx: number) => `Cultivar ${idx+1}`)
            let clusterLabels: number[] = [-1.0, -0.7, -0.3, 0, 0.3, 0.7, 1.0]

            const myColor = d3.scaleSequential()
                .interpolator(d3.interpolateInferno)
                .domain([-1, 1])
            let colorScale = myColor

            const rectSize = 12;
            const titleHeight = 20;

            const legendGroups = legendContainer.append('g')
                .attr('transform', `translate(0, ${titleHeight})`)
                .selectAll('g')
                .data<number>(clusterLabels)
                .join((enter) => {
                    let select = enter.append('g');

                    select.append('rect')
                        .attr('width', rectSize).attr('height', rectSize)
                        .attr('x', 5).attr('y', (d: number, idx: number) => idx * rectSize * 1.5)
                        .style('fill', (d: number) => myColor(d) as string)

                    select.append('text')
                        .text((d: number) => d)
                        .style('font-size', '.7rem')
                        .style('text-anchor', 'start')
                        .attr('x', rectSize)
                        .attr('y', (d: number, idx: number) => idx * rectSize * 1.5)
                        .attr('dx', '0.7rem')
                        .attr('dy', '0.7rem')
                    return select
                })

            const title = legendContainer
                .append('text')
                .style('font-size', '.7rem')
                .style('text-anchor', 'start')
                .style('font-weight', 'bold')
                .text('Correlations')
                .attr('x', 5)
                .attr('dy', '0.7rem')
        },
    },
    watch: {
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#scatter-bean2-svg').selectAll('*').remove() // Clean all the elements in the chart
                this.initChart()
                this.initLegend()
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
        <svg id="scatter-bean2-svg" width="100%" height="100%">
            <!-- all the visual elements we create in initChart() will be inserted here in DOM-->
        </svg>
        <svg id="heatmap-legend-svg" width="50%" height="80%">
        </svg>
    </div>

    <div id="scatter-control-container2" class="d-flex">
        </div>
    
</template>

<style scoped>
.chart-container{
    height: 100%;
}
#scatter-control-container2{
    width: 6rem;
    flex-direction: column;
}
</style>