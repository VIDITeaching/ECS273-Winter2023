
<template>
    <!-- <div class="outer" ref="parallelContainer">
            <div class="inner"><svg id="stacked-svg"></svg></div>
        </div> -->
    <div ref="parallelContainer" class="chart-container outer d-flex">

        <svg id="stacked-svg" class="inner"></svg>
    </div>
</template>
  
<script lang="ts">
import * as d3 from 'd3';
import axios from 'axios';
import { mapState, storeToRefs } from 'pinia';
import { useHousingStore } from '../stores/housingStore';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';

interface DataPoint {
    year: number;
    [key: string]: number;
}

export default {
    setup() {
        const store = useHousingStore();
        const { resize } = storeToRefs(store);
        return {
            store,
            resize
        }
    },
    computed: {
        ...mapState(useHousingStore, ['selectedMethod'])
    },

    created() {
        this.store.fetchHousing(this.selectedMethod);
    },
    methods: {

        onResize() {
            let target = this.$refs.parallelContainer as HTMLElement

            if (target === undefined || target === null) return;
            this.store.size = { width: target.clientWidth, height: target.clientHeight };
        },


        async initChart() {

            let svg = d3.select('#stacked-svg')
                .attr('width', this.store.size.width + this.store.margin.left + this.store.margin.right)
                .attr('height', this.store.size.height + this.store.margin.top + this.store.margin.bottom)
                .append("g")
                .attr("transform", `translate(${this.store.margin.left}, ${-this.store.margin.bottom})`);



            // const svg = d3.select("#myviz")
            //     .append("g")

            //     .attr("width", this.store.size.width + this.store.margin.left + this.store.margin.right)
            //     .attr("height", this.store.size.height + this.store.margin.top + this.store.margin.bottom)
            //     .append("g")
            //     .attr("transform",
            //         `translate(${this.store.margin.left}, ${this.store.margin.top})`);

            // let csv = await axios.get(`${server}/fetchRents`);
            let data: any[] = d3.csvParse(this.store.housing);
            // let data: DataPoint[] = d3.csvParse(csv.data);

            const keys = data.columns.slice(1);


            const test = () => {
                let extent = 
            d3.extent(data, function (d: DataPoint) { 
                    
                    console.log('d.year: ', d.year)
                    return d.year; })

                    console.log('extent: ', parseInt(extent[1]) + 1)

                    console.log(getMax(data))
            }
            test()

            const x = d3.scaleLinear()
                .domain(d3.extent(data, function (d: DataPoint) { 
                    
                    // console.log('d.year: ', d.year)
                    return d.year; }))
                .range([this.store.margin.left, this.store.size.width - this.store.margin.right]);

            svg.append("g")
                .attr("transform", `translate(0, ${this.store.size.height})`)

                .call(d3.axisBottom(x).ticks(10).tickFormat(d3.format("")));

            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", (this.store.size.width  + this.store.margin.left ) / 2)
                .attr("y", this.store.size.height + this.store.margin.bottom - 3)
                .text("Year");
            var maxValue = d3.max(data, function (d) {
                var values = Object.values(d);
                values.shift(); // remove first element "year"
                return d3.max(values.map(Number));
            });



            function getMax(data: any) {
                let maxRow = data.reduce((maxRow: any, currentRow: any) => {
                    let currentRowSum = d3.sum(Object.values(currentRow).map(Number));
                    let maxRowSum = d3.sum(Object.values(maxRow).map(Number));
                    return currentRowSum > maxRowSum ? currentRow : maxRow;
                });
                let maxValue = d3.sum(Object.values(maxRow).map(Number));
                return maxValue;
            }


            function getMin(data: any) {
                let maxRow = data.reduce((maxRow: any, currentRow: any) => {
                    let currentRowSum = d3.sum(Object.values(currentRow).map(Number));
                    let maxRowSum = d3.sum(Object.values(maxRow).map(Number));
                    return currentRowSum > maxRowSum ? currentRow : maxRow;
                });
                let maxValue = d3.sum(Object.values(maxRow).map(Number));
                return maxValue;
            }




            const y = d3.scaleLinear()
                .domain([0, getMax(data)])
                .range([this.store.size.height, this.store.margin.top]);

            svg.append("g")
                .call(d3.axisLeft(y))
                .attr("transform", `translate(${this.store.margin.left}, 0)`);

            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", -this.store.size.height / 2 + (this.store.margin.bottom))
                .attr("y", (this.store.margin.left) - 75)
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-90)")
                .text("New Housing Production")

            const color = d3.scaleOrdinal(d3.schemeCategory10)
            
                .domain(keys)
                .range(d3.schemeTableau10)

            const stackedData = d3.stack()
            // .offset(d3.stackOffsetSilhouette)
                .keys(keys)
                .value((d,key) => {
                    return d[key] < 0 ? 0: d[key];
                })(data)
                

            // Add a clipPath: everything out of this area won't be drawn.
            const clip = svg.append("defs").append("svg:clipPath")
                .attr("id", "clip")
                .append("svg:rect")
                .attr("width", this.store.size.width )
                .attr("height", this.store.size.height )
                .attr("x", 0)
                .attr("y", 0);

            // Add brushing
            const brush = d3.brushX()                 // Add the brush feature using the d3.brush function
                .extent([[0, 0], [this.store.size.width, this.store.size.height]])
                .on("end", function (event, d) {

                }) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
            // .on("end", updateChart) // Each time the brush selection changes, trigger the 'updateChart' function

            // Create the scatter variable: where both the circles and the brush take place
            const areaChart = svg.attr("class", "brush")
                //   
                .append('g')
                .call(brush)
                .attr("clip-path", "url(#clip)")

            areaChart
                .selectAll("mylayers")

                .data(stackedData)
                .join("path")

                .attr("class", function (d) {
                    return "myArea " + d.key.replaceAll(' ', '')
                })
                .style("fill", function (d) {
                    return color(d.key);
                })
                .attr("d", d3.area()
                    .x((d: any, i: any) => x(d.data.year))
                    .y0((d: any) => y(d[0]))
                    .y1((d: any) => y(d[1]))
                )

                .on("mouseover", function (event, d) {
   
                    highlight(d.key.replaceAll(' ', ''))
                    tooltip.html(
                        `<div>County: ${d.key}</div>`
                    )
                        .style('visibility', 'visible');
                })
                .on('mousemove', function (event, d) {
                    tooltip
                        .style('top', (event.pageY - 10) + 'px')
                        .style('left', (event.pageX + 10) + 'px');

                    // get the x and y position of the mouse
                    // var x = event.clientX - chart.getBoundingClientRect().left;
                    // var y = event.clientY - chart.getBoundingClientRect().top;

                })
                .on("mouseleave", function (event, d) {
                    noHighlight(d.key.replaceAll(' ', ''))
                    tooltip.html(``).style('visibility', 'hidden');
                })
            // .attr('height', '90%')
            // .attr('width', '90%')
            // .attr("transform", `translate(${this.store.margin.left}, ${-this.store.margin.bottom})`);



            //////////
            // HIGHLIGHT GROUP //
            //////////

            let tooltip = d3
                .select('body')
                .append('div')
                .attr('class', 'd3-tooltip')
                .style('position', 'absolute')
                .style('z-index', '10')
                .style('visibility', 'hidden')
                .style('padding', '10px')
                .style('background', 'rgba(0,0,0,0.6)')
                .style('border-radius', '4px')
                .style('color', '#fff')
                .text('a simple tooltip');


            // What to do when one group is hovered
            var highlight = function (d: any) {
                // reduce opacity of all groups
                d3.selectAll(".myArea").style("opacity", .25)
                // expect the one that is hovered
                d3.select("." + d)
                .style("stroke", "black").style("opacity", 1)

            }

            // And when it is not hovered anymore
            var noHighlight = function (d: any) {
                d3.selectAll(".myArea").style("opacity", 1).style("stroke", "none")
            }


        },

        rerender() {

            d3.select('#stacked-svg').selectAll('*').remove() // Clean all the elements in the chart
            // d3.select('#my_dataviz').selectAll('*').remove()
            this.initChart()
        }
    },
    mounted() {
        window.addEventListener('resize', debounce(this.onResize, 100))
        this.onResize()
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    },

    watch: { // updated because a legend is added.

        resize(newSize) { // when window resizes
            if ((newSize.width !== 0) && (newSize.height !== 0)) {
                this.rerender()
            }
        },
        'store.housing'(data) { // when data changes
            if (!isEmpty(data)) {
                this.rerender()
            }
        },

        selectedMethod(newMethod) { // function triggered when a different method is selected via dropdown menu
            this.store.fetchHousing(newMethod)
        },
    }
}
</script>


<style scoped>
.chart-container {
    height: 100%;
    flex-direction: column;
    flex-wrap: center;
    width: 100%;

    border: 1px solid black; /* adds a 1px black border */
}


.method-select {
    outline: solid;
    outline-width: 1px;
    outline-color: lightgray;
    border-radius: 2px;
    width: 100%;
    padding: 2px 5px;
}

.outer {
    display: flex;
    justify-content: center;
    align-items: center;
    /* background-color: red; */
    height: 500px;
}
</style>