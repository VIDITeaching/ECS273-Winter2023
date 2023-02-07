<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';

import {  ComponentSize, Margin } from '../types';
interface Data { 
    Area: number,
    Perimeter: number,
    MajorAxisLength: number,
    MinorAxisLength: number,
    AspectRation: number,
    Eccentricity: number,
    ConvexArea: number,
    EquivDiameter: number,
    Extent: number,
    Solidity: number,
    roundness: number,
    Compactness: number,
    ShapeFactor1: number,
    ShapeFactor2: number,
    ShapeFactor3: number,
    ShapeFactor4: number,
    Class: number
}

export default {
    data() {
        return {
            data: [] as Data[],
            groups: [] as string[],
            dimensions: [] as string[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 20, right: 20, top: 20, bottom: 80} as Margin,
        }
    },
    computed: {
        rerender() {
            return (!isEmpty(this.data)) && this.size
        }
    },
    created() {
        axios.get(`${server}/fetchRaw`)
            .then(resp => {
                this.data = resp.data.data; 
                this.groups = resp.data.clusters;
                this.dimensions = resp.data.dimensions;
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        onResize() { 
            let target = this.$refs.linearContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: 0.9 * target.clientWidth, height: 0.9 * target.clientHeight }
            //this.size = { width: 600, height: 640 };
        },
        initChart() {
            var dimensions = this.dimensions
            var data = this.data
            var groups = this.groups
            var size = this.size
            var margin = this.margin

            var svg = d3.select("#linear-svg")
                .append("svg")
                    .attr("width", size.width + margin.left + margin.right)
                    .attr("height", size.height + margin.top + margin.bottom)
                .append("g")
                    .attr("transform","translate(" + margin.left + "," + margin.top + ")")
            
            var color = d3.scaleOrdinal()
                .domain(groups)
                .range(d3.schemeTableau10);
            
            var y = {}
            dimensions.forEach((attr)=>{
                let Extents = d3.extent(data.map((d: Data) => d[attr] as number)) as [number, number]
                y[attr] = d3.scaleLinear()
                    .domain(Extents)
                    .range([size.height, 0])
            })

            var x = d3.scalePoint()
                .range([0, size.width])
                .domain(dimensions)
            
            const highlight = function(d: Object) {
                d3.selectAll(".line")
                    .transition()
                    .style("opacity", '0.01')
                //@ts-ignore
                let class_name = this.dataset.class
                d3.selectAll("." + class_name)
                    .transition().duration(200)
                    .style("stroke", color(class_name) as string)
                    .style("opacity", '1')
            }

            const normal = function(d: Object) {
                d3.selectAll(".line")
                    .data(data)
                    .transition().duration(200).delay(1000)
                    .style("stroke", (d) => { return color(groups[d.Class]) as string})
                    .style("opacity", '0.2')
            }

            function path(d: Object) {
                //@ts-ignore
                return d3.line()(dimensions.map((p) => [x(p), y[p](d[p])]))
            }

            svg.selectAll("path")
                .data(data)
                .enter()
                .append("path")
                .attr("class",  (d) => { return "line " + groups[d.Class] as string})
                .attr("data-class", (d) => { return groups[d.Class] as string})
                .attr("d", path)
                .style("fill", "none")
                .style("stroke", (d) => { return color(groups[d.Class]) as string})
                .style("opacity", '0.2')
                .on("mouseover", highlight)
                .on("mouseout", normal)

            svg.selectAll("axis")
                .data(dimensions).enter()
                .append("g")
                .attr("class", "axis")
                .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
                .each(function(d) { d3.select(this).call(d3.axisLeft(y[d]).ticks(5)); })
                .append("text")
                .style("text-anchor", "middle")
                .attr("y", -9)
                .text((d) => d)
                .style("fill", "black")
            
            svg.append('text') 
                .attr('transform', `translate(${this.size.width / 2}, ${this.size.height + 10})`)
                .attr('dy', '0.5rem')
                .attr('dx', '0.5rem')
                .style('text-anchor', 'middle')
                .style('font-weight', 'bold')
                .text('Dry Bean Dataset Parallel Coordinates')

        }
    },
    watch: {
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#linear-svg').selectAll('*').remove()
                this.initChart()
            }
        }
    },
    mounted() {
        window.addEventListener('resize2', debounce(this.onResize, 100)) 
        this.onResize()
    },
    beforeDestroy() {
       window.removeEventListener('resize2', this.onResize)
    }
}
</script>

<template>
    <div class="chart-container d-flex" ref="linearContainer">
        <svg id="linear-svg" width="100%" height="100%"></svg>
    </div>
</template>

<style scoped>
.chart-container{
    width: 100%;
    height: 100%;
}
</style>