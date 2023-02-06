<script lang='ts'>
import * as d3 from 'd3';
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
import { cluster } from 'd3';
import { createStructuralDirectiveTransform } from '@vue/compiler-core';

interface RentData {
  post_id: string;
  date: number;
  year: number;
  nhood: string;
  city: string;
  county: string;
  price: number;
  beds: number;
  baths: number | null;
  sqft: number | null;
  room_in_apt: number;
  address: number | null;
  lat: number | null;
  lon: number | null;
  title: string;
  descr: number | null;
  details: number | null;
}    

/* The new major things from Example.vue
1) initLegend() in this component
2) the template and the css in this component
*/

export default {
    data() {
        return {
            rentData: [] as RentData[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 40, right: 50, top: 20, bottom: 50} as Margin,
        }
    },
    computed: {
        rerender() {
            return (!isEmpty(this.rentData)) && this.size
        }
    },
    created() {
        console.log('create');
        axios.post(`${server}/fetchTinyRent2`)
            .then(resp => {
                // console.log(resp.data);
                this.rentData = resp.data.data;
                this.initChart()
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
            let chartContainer = d3.select('#scatter-svg');
            // let xExtents = d3.extent(Object.values(this.rentData).map(d => new Date(d.date)));
            let xExtents = d3.extent(this.rentData.map(d => new Date(d.date)));
            let yExtents = d3.extent(this.rentData.map(d => d.price));
            let zExtents = d3.extent(this.rentData.map(d => d.sqft));

            let xScale = d3.scaleTime()
            .range([this.margin.left, this.size.width - this.margin.right])
            .domain(xExtents).nice();

            let yScale = d3.scaleLinear()
            .range([this.size.height - this.margin.bottom, this.margin.top])
            .domain(yExtents).nice();

            let scale = 100;
            let zScale = d3.scaleLinear()
            .range([1, 16])
            .domain(zExtents);
            console.log(zScale);

            const xAxis = chartContainer.append('g')
            .attr('transform', `translate(0, ${this.size.height - this.margin.bottom})`)
            .call(d3.axisBottom(xScale));

            const yAxis = chartContainer.append('g')
            .attr('transform', `translate(${this.margin.left}, 0)`)
            .call(d3.axisLeft(yScale));

            const yLabel = chartContainer.append('g')
            .attr('transform', `translate(${this.margin.left}, ${this.size.height / 2 + this.margin.top}) rotate(-90)`)
            .append('text')
            .text('Price');

            const xLabel = chartContainer.append('g')
            .attr('transform', `translate(${this.size.width / 2}, ${this.size.height - this.margin.top})`)
            .append('text')
            .text('Date');
            let colors = ['#051c33', '#0c4c6f', '#1379a8', '#45aebf', '#85c9a8', '#a9d185']

            let colorScale = d3.scaleOrdinal().domain(d3.extent(this.rentData, (d) => d.beds)).range(colors) // d3.schemeTableau10: string[]
            const points = chartContainer.append('g')
            .selectAll('circle')
            .data(this.rentData)
            .join('circle')
            .attr('cx', (d) => xScale(new Date(d.date)))
            .attr('cy', (d) => yScale(d.price))
            .attr('r', (d) => zScale(d.sqft))
            .style('fill', (d) => colorScale(String(d.beds)) as string)
            .style('opacity', .7);

            const title = chartContainer.append('g')
            .append('text')
            .attr('transform', `translate(${this.size.width / 2}, ${this.size.height - this.margin.top})`)
            .attr('dy', '0.5rem')
            .style('text-anchor', 'middle')
            .style('font-weight', 'bold')
            .text('Rent Prices Over Time');
        },
        initLegend() {
            let legendContainer = d3.select('#scatter-legend-svg')

            let clusterLabels: string[] = this.rentData.map((d) => `# of beds: ${d.beds}`)
            let sortedClusterLabels = clusterLabels.sort((a, b) => {
                let bedsA = Number(a.split(':')[1].trim());
                let bedsB = Number(b.split(':')[1].trim());
                return bedsB - bedsA;
            });
            console.log('labels: ', clusterLabels);
            clusterLabels = Array.from(new Set(clusterLabels));
            console.log('labels: ', clusterLabels);
            let colors = ['#051c33', '#0c4c6f', '#1379a8', '#45aebf', '#85c9a8', '#a9d185']

            let colorScale = d3.scaleOrdinal().domain(clusterLabels).range(colors)

            const rectSize = 12;
            const titleHeight = 20;

            // This is further utilizing data joins in d3.js, you can find the equivalent code in the comments below.
            // Check out https://observablehq.com/@d3/selection-join
            const legendGroups = legendContainer.append('g')
                .attr('transform', `translate(0, ${titleHeight})`) // this is applied to 'g' element and will affect all the child elements.
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
                },
                )
            
            const title = legendContainer
                .append('text')
                .style('font-size', '.7rem')
                .style('text-anchor', 'start')
                .style('font-weight', 'bold')
                .text('Beds')
                .attr('x', 5)
                .attr('dy', '0.7rem')
        }
    },
    watch: {
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#scatter-svg').selectAll('*').remove()
                d3.select('#scatter-legend-svg').selectAll('*').remove()
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

<!-- We use flex to arrange the layout-->
<template>
    <div class='viz-container d-flex justify-end'>
        <div class='chart-container d-flex' ref='scatterContainer'>
            <svg id='scatter-svg' width='100%' height='100%'>
            </svg>
        </div>
        <div id='scatter-legend-container' class='d-flex'>
            <svg id='scatter-legend-svg' width='100%' height='100%'>
            </svg>
        </div>
    </div>
</template>

<!-- How we arrange the two svgs with css-->
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
#scatter-legend-container{
    width: 6rem;
    flex-shrink: 0;
    overflow: auto;
}
</style>