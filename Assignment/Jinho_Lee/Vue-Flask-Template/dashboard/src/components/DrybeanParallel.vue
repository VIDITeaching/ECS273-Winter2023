<!DOCTYPE html>
<meta charset="utf-8">

<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';
import { legend as Legend } from "@d3/color-legend"
import { Point, ComponentSize, Margin } from '../types';
interface ScatterPoint extends Point{
    cluster: string;
}
interface DryBean {
    // Area: number;
    // Perimeter: number;
    // MajorAxisLength: number;
    // MinorAxisLength: number;
    // AspectRation: number;
    Eccentricity: number;
    ConvexArea: number;
    EquivDiameter: number;
    Extent: number;
    // Solidity: number;
    // roundness: number;
    // Compactness: number;
    // ShapeFactor1: number;
    // ShapeFactor2: number;
    // ShapeFactor3: number;
    // ShapeFactor4: number;
    Class: string;
}

/* The new major things from Example.vue
1) initLegend() in this component
2) the template and the css in this component
*/

export default {
    data() {
        return {
            points: [] as ScatterPoint[],
            columns: [] as string[],
            bean_data: [] as DryBean[],
            clusters: [] as string[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 60, right: 20, top: 20, bottom: 60} as Margin,
        }
    },
    computed: {
        rerender() {
            return (!isEmpty(this.bean_data))  && this.size
        }
    },
    created() {
        axios.post(`${server}/fetchExample`, {method: 'parallel'})
            .then(resp => {
                this.bean_data = resp.data.data;
                this.clusters = resp.data.clusters;
                this.columns = resp.data.columns;

                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        onResize() {
            let target = this.$refs.scatterContainer as HTMLElement
            if (target === undefined || target === null) return;
            this.size = { width: target.clientWidth, height: target.clientHeight };
        },

        initChart() {
            var margin = {top: 50, right: 10, bottom: 100, left: 10},
                            width = this.size.width - margin.left - margin.right,
                            height = this.size.height - margin.top - margin.bottom;

            var svg = d3.select("#parallel-svg")
                .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

            // let matrix_columns = ["Area", "AspectRation", "Compactness", "ConvexArea", "Class"];
            let domain_org = this.columns;
            
            // const domain_org = this.clusters;
            // const domain_org: string[] = this.clusters;
            const domains = d3.csvParse(domain_org.join(','));
            // const domains = d3.csvParse(domain_org.join(','));
            const domains_len = domains.length;
            console.log('lomg data');

            const data = this.bean_data;

            let dimensions = domains['columns'].filter(function(d) { return d != "Class" })
            // let dimensions = Object.keys(data[0]).filter(function(d) { return d != "Class" })

            // For each dimension, I build a linear scale. I store all in a y object
            let y = {}
            for (let i in domain_org) {
                let name = dimensions[i]
                y[name] = d3.scaleLinear()
                    .domain( d3.extent(data, function(d) { return +d[name]; }) )
                    .range([height, 0])
            }
            console.log(y)

            // Build the X scale -> it find the best position for each Y axis
            let x = d3.scalePoint()
                .range([0, width])
                .padding(1)
                .domain(dimensions);

            console.log(x);
            console.log(dimensions)

            const color = d3.scaleOrdinal()
                .domain(dimensions)
                .range(d3.schemeTableau10)

            const highlight = function(event, d){
                const selected_class = d.Class

                // first every group turns grey
                d3.selectAll(".line")
                    .transition().duration(200)
                    .style("stroke", "lightgrey")
                    .style("opacity", "0.2")
                // Second the hovered specie takes its color
                d3.selectAll("." + selected_class)
                    .transition().duration(200)
                    .style("stroke", color(selected_class))
                    .style("opacity", "1")
            }

            // Unhighlight
            const doNotHighlight = function(event, d){
                d3.selectAll(".line")
                    .transition().duration(200).delay(1000)
                    .style("stroke", function(d){ return( color(d.Class))} )
                    .style("opacity", "1")
            }

            // The path function take a row of the csv as input, and return x and y coordinates of the line to draw for this raw.
            function path(d) {
                return d3.line()(dimensions.map(function(p) { return [x(p), y[p](d[p])]; }));
            }

            // Draw the lines
            const paths = svg.selectAll("myPath")
                .data(data)
                .join("path")
                    .attr("d", path)
                    .attr("class", function (d) { return "line " + d.Class } )
                    .attr("stroke-width", 0.3)
                    .style("fill", "none")
                    .style("stroke", function(d){ return( color(d.Class))} )
                    .style("opacity", 0.3)
                    .on("mouseover", highlight)
                    .on("mouseleave", doNotHighlight )

            // Draw the axis:
            const Axis = svg.selectAll("myAxis")
                .data(dimensions).enter()
                .append("g")
                .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
                .each(function(d) { d3.select(this).call(d3.axisLeft().scale(y[d])); })
                .append("text")
                    .style("font", "bold 12px sans-serif")
                    .style("text-anchor", "middle")
                    .attr("y", -9)
                    .text(function(d) { return d; })
                        .style("fill", "black")
            
            const title = svg.append('g')
                .append('text') // adding the text
                .attr('transform', `translate(${width / 2}, ${height+20})`)
                .attr('dy', '0.5rem') // relative distance from the indicated coordinates.
                .style("font", "bold 15px sans-serif")
                .style('text-anchor', 'middle')
                .style('font-weight', 'bold')
                .text('Dry bean - Parallel Coordinate') // text content                
    },
        initLegend() {
            let legendContainer = d3.select('#parallel-legend-svg');

            // let clusterLabels: string[] = this.clusters.map((cluster: string, idx: number) => `Cultivar ${idx+1}`)
            let clusterLabels: string[] = this.clusters
            let colorScale = d3.scaleOrdinal().domain(clusterLabels).range(d3.schemeTableau10)

            const rectSize = 12;
            const titleHeight = 20;

            // This is further utilizing data joins in d3.js, you can find the equivalent code in the comments below.
            // Check out https://observablehq.com/@d3/selection-join
            const legendGroups = legendContainer.append('g')
                .attr('transform', `translate(0, ${titleHeight})`) // this is applied to "g" element and will affect all the child elements.
                .selectAll('g')
                .data<string>(clusterLabels)
                .join((enter) => { // This enter syntax is recommended when you want to join multiple non-nested elements per data point
                    // This callback here is for newly added elements.
                    let select = enter.append('g');

                    select.append('rect')
                        .attr('width', rectSize).attr('height', rectSize)
                        .attr('x', 5).attr('y', (d: string, idx: number) => idx * rectSize * 1.5)
                        .style('fill', (d: string) => colorScale(d) as string)

                    select.append('text')
                        .text((d: string) => d)
                        .style('font-size', '.7rem')
                        .style('text-anchor', 'start')
                        .attr('x', rectSize)
                        .attr('y', (d: string, idx: number) => idx * rectSize * 1.5)
                        .attr('dx', '0.7rem')
                        .attr('dy', '0.7rem')
                    return select
                }, // you can add callbacks for updating elements and removing elements as other arguments here.
            )
            const title = legendContainer
                .append('text')
                .style('font-size', '.7rem')
                .style('text-anchor', 'start')
                .style('font-weight', 'bold')
                .text('Bean Type')
                .attr('x', 5)
                .attr('dy', '0.7rem')

        }
    },
    watch: { // updated because a legend is added.
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#parallel-svg').selectAll('*').remove()
                d3.select('#parallel-legend-svg').selectAll('*').remove()
                this.initChart()
                this.initLegend()
            }
        }
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

<!-- "ref" registers a reference to the HTML element so that we can access it via the reference in Vue.  -->
<!-- We use flex to arrange the layout-->
<template>
    <div class="chart-container d-flex" ref="scatterContainer">
        <svg id="parallel-svg" width="100%" height="100%">
            <!-- all the visual elements we create in initChart() will be inserted here in DOM-->
        </svg>
        <div id="scatter-control-container" class="d-flex">
            <svg id="parallel-legend-svg" width=100 height="40%">
            </svg>
        </div>

    </div>


</template>

<style scoped>
.viz-container{
    height:100%;
    flex-direction: row;
    flex-wrap: nowrap;
}
.chart-container{
    width: calc(100% - 5rem);
    height: 100%;
}

#parallel-legend-container{
    width: 5rem;
}
</style>