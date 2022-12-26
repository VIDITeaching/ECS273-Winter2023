<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
interface ScatterPoint extends Point{
    cluster: string;
}

export default {
    data() {
        return {
            points: [] as ScatterPoint[],
            clusters: [] as string[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 20, right: 20, top: 20, bottom: 40} as Margin,
        }
    },
    computed: {
        // Re-render the chart whenever the window is resized or the data changes (and data is non-empty)
        rerender() {
            return (!isEmpty(this.points)) && this.size.width && this.size.height
        }
    },
    created() {
        axios.get(`${server}/fetchExample`)
            .then(resp => {
                this.points = resp.data.data;
                this.clusters = resp.data.clusters;
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        onResize() {
            let target = this.$refs.scatterContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: target.clientWidth, height: target.clientHeight };
        },
        initChart() {
            let chartContainer = d3.select('#scatter-svg')

            let xExtents = d3.extent(this.points.map((d: ScatterPoint) => d.posX as number)) as [number, number]
            let yExtents = d3.extent(this.points.map((d: ScatterPoint) => d.posY as number)) as [number, number]

            let xScale = d3.scaleLinear()
                .range([this.margin.left, this.size.width - this.margin.right])
                .domain(xExtents)

            let yScale = d3.scaleLinear()
                .range([this.size.height - this.margin.bottom, this.margin.top])
                .domain(yExtents)

            let clusters: string[] = this.clusters.map((cluster: string, idx: number) => String(idx))
            let colorScale = d3.scaleOrdinal().domain(clusters).range(d3.schemeTableau10) // d3.schemeTableau10: string[]

            const points = chartContainer.append('g')
                .selectAll('circle')
                .data<ScatterPoint>(this.points)
                .join('circle')
                .attr('cx', (d: ScatterPoint) => xScale(d.posX))
                .attr('cy', (d: ScatterPoint) => yScale(d.posY))
                .attr('r', 5)
                .style('fill', (d: ScatterPoint) => colorScale(String(d.cluster)) as string)
                .style('opacity', .7)

            const title = chartContainer.append('g')
                .append('text')
                .attr('transform', `translate(${this.size.width / 2}, ${this.size.height - this.margin.top})`)
                .attr('dy', '0.5rem')
                .style('text-anchor', 'middle')
                .style('font-weight', 'bold')
                .text('Wine Dataset PCA Projection')
        },
    },
    watch: {
        rerender(signal) {
            if (signal) {
                d3.select('#scatter-svg').selectAll('*').remove() // Clean all the elements in the chart
                this.initChart()
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

<template>
    <div class="chart-container d-flex" ref="scatterContainer">
        <svg id="scatter-svg" width="100%" height="100%">
        </svg>
    </div>
</template>

<style scoped>
.chart-container{
    height: 100%;
}
</style>