<script lang="ts">
import * as d3 from "d3";
import { debounce, isEmpty } from 'lodash';

// For importing a store. See how it's set up in ./dashboard/stores/ and ./dashboard/main.ts
import { mapState, storeToRefs } from 'pinia';
import { useStore } from '../stores/BarStore';

export default {
    setup() { // Composition API syntax
        const store = useStore()
        // Alternative expression from computed
        const { resize } = storeToRefs(store);
        return {
            store, // Return store as the local state, but when you update the property value, the store is also updated.
            resize,
        }
    },
    computed: {
        ...mapState(useStore, ['selectedMethod']) // Traditional way to map the store state to the local state
    },
    created() {
        this.store.fetchExample(this.selectedMethod);
    },
    methods: {
        onResize() {
            let target = this.$refs.barContainer as HTMLElement
            if (target === undefined || target === null) return;
            this.store.size = { width: target.clientWidth, height: target.clientHeight }; // How you update the store
        },
        initChart() {
            // Create an empty (detached) chart container.
            let chartContainer = d3.select('#right-bar-svg');

            let xScale = d3.scaleBand()
                .range([this.store.margin.left, this.store.size.width]) // left side to the right side on the screen
                .domain(this.store.emotion)
                .padding(0.2);

            let subXScale = d3.scaleBand()
                .domain(this.store.people)
                .range([0, xScale.bandwidth()]);

            // In viewport (our screen), the topmost side always refer to 0 in the vertical coordinates in pixels (y).
            let yScale = d3.scaleLinear()
                .range([this.store.size.height - this.store.margin.bottom, this.store.margin.top]) //bottom side to the top side on the screen
                .domain([0, 0.6]);

            let ppl: string[] = this.store.people.map((person: string, idx: number) => String(idx))
            let colorScale = d3.scaleOrdinal()
                .domain(ppl)
                .range(['#2ca02c', '#d62728', '#1f77b4']);

            const xAxis = chartContainer.append('g')
                .attr('transform', `translate(0, ${this.store.size.height - this.store.margin.bottom})`)
                .call(d3.axisBottom(xScale).tickSize(0));

            const yAxis = chartContainer.append('g')
                .attr('transform', `translate(${this.store.margin.left + 11}, 0)`)
                .call(d3.axisLeft(yScale));

            const xLabel = chartContainer.append('g')
                .attr('transform', `translate(${this.store.size.width / 2 - 15}, ${this.store.size.height - 15})`)
                .append('text')
                .style('font-size', '0.8rem')
                .text('Emotion');

            const yLabel = chartContainer.append('g')
                .attr('transform', `translate(${this.store.margin.left / 4 + 2}, ${this.store.size.height / 2 + this.store.margin.top}) rotate(-90)`)
                .append('text')
                .style('font-size', '0.8rem')
                .text('Score');

            // go through each key of the scores array:
            for (const key in this.store.scores) {

                // Get the indexed item by the key:
                var indexedItem = this.store.scores[key];
                const p = this.store.people;
                const e = this.store.emotion;
                const height = this.store.size.height;
                const bot_margin = this.store.margin.bottom;

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
                .attr("class", "title")
                .append('text')
                .attr('transform', `translate(${this.store.size.width / 2}, 0)`)
                .attr('dy', '1rem') // relative distance from the indicated coordinates.
                .style('font-size', '0.75rem')
                .style('text-anchor', 'middle')
                .style('font-weight', 'bold')
                .text('Emotion Breakdown on Surpreme Court Topic')
        },
        initLegend() {
            let legendContainer = d3.select('#bar-legend-svg')

            let ppl: string[] = this.store.people.map((person: string, idx: number) => String(idx))
            let colorScale = d3.scaleOrdinal()
                .domain(ppl)
                .range(['#4daf4a', '#e41a1c', '#377eb8']);

            const rectSize = 20;
            const titleHeight = 50;

            const legendGroups = legendContainer.append('g')
                .attr('transform', `translate(0, ${titleHeight})`) // this is applied to "g" element and will affect all the child elements.
                .selectAll('g')
                .data(this.store.people)
                .join((enter) => { // This enter syntax is recommended when you want to join multiple non-nested elements per data point
                    // This callback here is for newly added elements.
                    let select = enter.append('g');

                    select.append('rect')
                        .attr('width', rectSize).attr('height', rectSize)
                        .attr('x', 0).attr('y', (d: string, idx: number) => idx * rectSize * 1.3)
                        .style('fill', (d: string) => colorScale(d) as string)

                    select.append('text')
                        .text((d: string) => d)
                        .style('font-size', '0.9rem')
                        .style('text-anchor', 'start')
                        .attr('x', rectSize / 2)
                        .attr('y', (d: string, idx: number) => idx * rectSize * 1.5)
                        .attr('dx', '0.7rem')
                        .attr('dy', '0.7rem')
                    return select
                })
        },
        rerender() {
            d3.select('#right-bar-svg').selectAll('*').remove() // Clean all the elements in the chart
            d3.select('#bar-legend-svg').selectAll('*').remove()
            this.initChart()
            this.initLegend()
        },
        update_chart_title(topic: string) {
            d3.select('#right-bar-svg').selectAll('.title').remove()

            let chartContainer = d3.select('#right-bar-svg');
            const title = chartContainer.append('g')
                .attr("class", "title")
                .append('text')
                .attr('transform', `translate(${this.store.size.width / 2}, 0)`)
                .attr('dy', '0.6rem') // relative distance from the indicated coordinates.
                .style('font-size', '0.8rem')
                .style('text-anchor', 'middle')
                .style('font-weight', 'bold')
                .text('Emotion Breakdown on ' + topic + ' Topic')
        }
    },
    watch: {
        resize(newSize) { // when window resizes
            if ((newSize.width !== 0) && (newSize.height !== 0)) {
                this.rerender()
            }
        },
        'store.scores'(newScores) { // when data changes
            if (!isEmpty(newScores)) {
                this.rerender()
                //below is new
                this.update_chart_title(this.store.selectedMethod)
            }
        },
        selectedMethod(newMethod) { // function triggered when a different method is selected via dropdown menu
            this.store.fetchExample(newMethod)
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

<!-- We only use vanilla widgets here, you can use the equivalent components from the UI library -->
<!-- Helpful References: https://vuejs.org/guide/essentials/class-and-style.html#binding-html-classes -->
<template>
    <div class="viz-container d-flex justify-end">
        <div class="right-chart-container d-flex" ref="barContainer">
            <svg id="right-bar-svg" width="100%" height="100%">
            </svg>
        </div>

        <div id="bar-control-container" class="d-flex">
            <svg id="bar-legend-svg" width="100%" height="40%">
            </svg>
            <div class="d-flex mb-4">
                <label :style="{ fontSize: '1rem' }"> Select Topic:
                    <select class="method-select" v-model="store.selectedMethod">
                        <option v-for="method in store.methods" :value="method"
                            :selected="(method === store.selectedMethod) ? true : false">{{ method }}</option>
                    </select>
                </label>
            </div>
        </div>

    </div>
</template>

<style scoped>
.viz-container {
    height: 100%;
    flex-direction: row;
    flex-wrap: nowrap;
}

.right-chart-container {
    width: calc(100% - 7rem);
    height: 100%;
}

#bar-legend-container {
    width: 7rem;
}

#bar-control-container {
    width: 10rem;
    flex-direction: column;
}

.method-select {
    outline: solid;
    outline-width: 1px;
    outline-color: lightgray;
    border-radius: 2px;
    width: 100%;
    padding: 2px 5px;
}
</style>