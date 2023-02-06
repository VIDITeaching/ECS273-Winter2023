<script lang="ts">
import * as d3 from "d3";
import axios from 'axios'; // Library in Javascript to make HTTP requests from node.js or XMLhttpRequests from the browsers
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';

import { ComponentSize, Margin } from '../types';

export default {
    name: 'GroupBarChart',
    data() {
        return {
            scores: [],
            emotion: [] as string[],
            people: [] as string[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: { left: 50, right: 20, top: 40, bottom: 40 } as Margin,
        }
    },
    computed: {
        // Re-render the chart whenever the window is resized or the data changes (and data is non-empty)
        rerender() {
            return (!isEmpty(this.scores)) && this.size
        }
    },
    created() {
        axios.get(`${server}/fetchExample`)
            .then(resp => {
                this.scores = resp.data.data;
                this.emotion = resp.data.emotion;
                this.people = resp.data.people;
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        onResize() {
            // record the updated size of the target element
            let target = this.$refs.barContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: target.clientWidth, height: target.clientHeight };
        },
        initChart() {
            // Create an empty (detached) chart container.
            let chartContainer = d3.select('#bar-svg');

            let xScale = d3.scaleBand()
                .range([this.margin.left, this.size.width - this.margin.right]) // left side to the right side on the screen
                .domain(this.emotion)
                .padding(0.2);

            let subXScale = d3.scaleBand()
                .domain(this.people)
                .range([0, xScale.bandwidth()])
                .padding(0.05);

            // In viewport (our screen), the topmost side always refer to 0 in the vertical coordinates in pixels (y).
            var yMaxArr = d3.extent(this.scores.map(function (d, i) {
                return d[i];
            })) as [unknown, unknown]
            yMaxArr[0] = 0

            // console.log(yMaxArr)

            let yScale = d3.scaleLinear()
                .range([this.size.height - this.margin.bottom, this.margin.top]) //bottom side to the top side on the screen
                .domain([0, 0.6]);

            let ppl: string[] = this.people.map((person: string, idx: number) => String(idx))
            let colorScale = d3.scaleOrdinal()
                .domain(ppl)
                .range(['#4daf4a', '#e41a1c', '#377eb8']);

            const xAxis = chartContainer.append('g')
                .attr('transform', `translate(0, ${this.size.height - this.margin.bottom})`)
                .call(d3.axisBottom(xScale).tickSize(0));

            const yAxis = chartContainer.append('g')
                .attr('transform', `translate(${this.margin.left}, 0)`)
                .call(d3.axisLeft(yScale));

            const xLabel = chartContainer.append('g')
                .attr('transform', `translate(${this.size.width / 2 - 15}, ${this.size.height - 15})`)
                .append('text')
                .text('Emotion');

            const yLabel = chartContainer.append('g')
                .attr('transform', `translate(${this.margin.left / 4}, ${this.size.height / 2 + this.margin.top}) rotate(-90)`)
                .append('text')
                .text('Score');

            // go through each key of the scores array:
            for (const key in this.scores) {

                // Get the indexed item by the key:
                var indexedItem = this.scores[key];
                const p = this.people;
                const e = this.emotion;
                const height = this.size.height;
                const bot_margin = this.margin.bottom;

                var resultArray = Object.keys(indexedItem).map(function (idx) {
                    let score = indexedItem[idx]
                    return score;
                });

                const bars = chartContainer.append('g')
                    .selectAll('rect')
                    .data(resultArray)
                    .join('rect')
                    .attr("transform", function (_, i) { return "translate(" + xScale(e[key]) + ",0)"; })
                    .attr('x', (_, i) => subXScale(p[i]))
                    .attr("y", function (d) { return yScale(d); })
                    .attr('width', subXScale.bandwidth())
                    .attr('height', function (d) { return height - bot_margin - yScale(d); })
                    .style('fill', d => colorScale(String(d)) as string)
            }

            const title = chartContainer.append('g')
                .append('text')
                .attr('transform', `translate(${this.size.width / 2}, 0)`)
                .attr('dy', '1rem') // relative distance from the indicated coordinates.
                .style('text-anchor', 'middle')
                .style('font-weight', 'bold')
                .text('Emotion Breakdown on Surpreme Court Topic')
        },
        initLegend() {
            let legendContainer = d3.select('#bar-legend-svg')

            let ppl: string[] = this.people.map((person: string, idx: number) => String(idx))
            let colorScale = d3.scaleOrdinal()
                .domain(ppl)
                .range(['#4daf4a', '#e41a1c', '#377eb8']);

            const rectSize = 20;
            const titleHeight = 50;

            const legendGroups = legendContainer.append('g')
                .attr('transform', `translate(0, ${titleHeight})`) // this is applied to "g" element and will affect all the child elements.
                .selectAll('g')
                .data(this.people)
                .join((enter) => { // This enter syntax is recommended when you want to join multiple non-nested elements per data point
                    // This callback here is for newly added elements.
                    let select = enter.append('g');

                    select.append('rect')
                        .attr('width', rectSize).attr('height', rectSize)
                        .attr('x', 10).attr('y', (d: string, idx: number) => idx * rectSize * 1.3)
                        .style('fill', (d: string) => colorScale(d) as string)

                    select.append('text')
                        .text((d: string) => d)
                        .style('font-size', '1rem')
                        .style('text-anchor', 'start')
                        .attr('x', rectSize)
                        .attr('y', (d: string, idx: number) => idx * rectSize * 1.5)
                        .attr('dx', '0.7rem')
                        .attr('dy', '0.7rem')
                    return select
                }, // you can add callbacks for updating elements and removing elements as other arguments here.
                )
        }
    },
    watch: {
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#bar-svg').selectAll('*').remove() // Clean all the elements in the chart
                d3.select('#bar-legend-svg').selectAll('*').remove()
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
};
</script>

<!-- "ref" registers a reference to the HTML element so that we can access it via the reference in Vue.  -->
<!-- We use flex to arrange the layout-->
<template>
    <div class="viz-container d-flex justify-end">
        <div class="chart-container d-flex" ref="barContainer">
            <svg id="bar-svg" width="100%" height="100%">
            </svg>
        </div>
        <div id="bar-legend-container" class="d-flex">
            <svg id="bar-legend-svg" width="100%" height="100%">
            </svg>
        </div>
    </div>
</template>



<style scoped>
.viz-container {
    height: 100%;
    flex-direction: row;
    flex-wrap: nowrap;
}

.chart-container {
    width: calc(100% - 7rem);
    height: 100%;
}

#bar-legend-container {
    width: 7rem;
}
</style>