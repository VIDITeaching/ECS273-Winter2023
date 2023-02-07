<script lang="ts">
import * as d3 from 'd3';
import axios from 'axios';
import { server } from '../helper';
import { isEmpty, debounce, List } from 'lodash';
import { Point, ComponentSize, Margin } from '../types';

export default {
    data() {
        return {
            pieData: [{ name: 'SEKER', value: 2027 }, { name: 'BARBUNYA', value: 1322 }, { name: 'BOMBAY', value: 522 }, { name: 'CALI', value: 1630 }, { name: 'HOROZ', value: 1928 }, { name: 'SIRA', value: 2636 }, { name: 'DERMASON', value: 3546 }] as List,
        }
    },
    created() {
        axios.get(`${server}/fetchPie`)
            .then(resp => { // check out the app.py in ./server/ to see the format
                // console.log(typeof (resp.data.data), resp.data.data)
                this.pieData = resp.data.data;
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        getpiedata() {
            axios.get(`${server}/fetchPie`)
                .then(resp => { // check out the app.py in ./server/ to see the format
                    console.log(typeof (resp.data.data), resp.data.data)
                    return resp.data.data;
                    return true;
                })
                .catch(error => console.log(error));
        },
        drawPieChart() {
            const svg = d3.select(this.$refs.pieChart);
            const width = +svg.attr('width');
            const height = +svg.attr('height');
            const radius = Math.min(width, height) / 2;

            const color = d3.scaleOrdinal(d3.schemeCategory10);
            const pie = d3.pie().value(d => d.value);

            console.log('piedata', this.pieData);
            const data = pie(this.pieData);

            const g = svg.append('g')
                .attr('transform', `translate(${width / 2}, ${height / 2})`);

            const arc = d3.arc()
                .innerRadius(0)
                .outerRadius(radius);

            const arcs = g.selectAll('.arc')
                .data(data)
                .enter().append('g')
                .attr('class', 'arc');

            arcs.append('path')
                .attr('d', arc)
                .style('fill', d => color(d.data.name));
        },
        initLegend() {
            let legendContainer = d3.select('#pie-legend-svg')
            let clusterLabels: string[] = ['SEKER', 'BARBUNYA', 'BOMBAY', 'CALI', 'HOROZ', 'SIRA', 'DERMASON'] //this.clusters.map((cluster: string, idx: number) => `Cultivar ${idx + 1}`)
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
                .text('Cultivars')
                .attr('x', 5)
                .attr('y', 5)
                .attr('dy', '0.7rem')
        }
    },

    mounted() {
        this.drawPieChart();
        this.initLegend();
    }
};
</script>

<template>
    <div>
        <svg ref="pieChart" width="350" height="350"></svg>
    </div>
    <div id="scatter-legend-container" class="d-flex">
        <svg id="pie-legend-svg" width="100%" height="100%">
        </svg>
    </div>
</template>

<style scoped>
.viz-container {
    height: 100%;
    flex-direction: row;
    flex-wrap: nowrap;
}

.chart-container {
    width: calc(100% - 5rem);
    height: 100%;
}

#scatter-legend-container {
    width: 5rem;
}
</style>