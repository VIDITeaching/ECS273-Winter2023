
<template>
        <!-- <div class="outer" ref="parallelContainer">
            <div class="inner"><svg id="stacked-svg"></svg></div>
        </div> -->
        <div ref="parallelContainer" class="chart-container outer d-flex" >
            
            <svg id="stacked-svg" class = "inner"></svg>
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
            
            console.log('resize: ', target.clientWidth)
            if (target === undefined || target === null) return;
            this.store.size = { width: target.clientWidth, height: target.clientHeight };
        },


        async initChart() {

            console.log('otherstore.size: ', this.store.size)
            let svg = d3.select('#stacked-svg')
                .attr('width', this.store.size.width + this.store.margin.left + this.store.margin.right)
                .attr('height', this.store.size.height + this.store.margin.top + this.store.margin.bottom)
                .append("g")
                .attr("transform", `translate(${this.store.margin.left}, ${-this.store.margin.bottom})`);
                    
            console.log('this.store.margin: ', this.store.margin)
            console.log('this.store.size: ', this.store.size)


            console.log('idk: ', this.store.size.width + this.store.margin.left + this.store.margin.right)

            // const svg = d3.select("#myviz")
            //     .append("g")

            //     .attr("width", this.store.size.width + this.store.margin.left + this.store.margin.right)
            //     .attr("height", this.store.size.height + this.store.margin.top + this.store.margin.bottom)
            //     .append("g")
            //     .attr("transform",
            //         `translate(${this.store.margin.left}, ${this.store.margin.top})`);

            // let csv = await axios.get(`${server}/fetchRents`);
            // console.log('data: ', this.store.housing)
            let data: any[] = d3.csvParse(this.store.housing);
            // let data: DataPoint[] = d3.csvParse(csv.data);

            const keys = data.columns.slice(1);

            const x = d3.scaleLinear()
                .domain(d3.extent(data, function (d: DataPoint) { return d.year; }))
                .range([0, this.store.size.width]);
                
            svg.append("g")
                .attr("transform", `translate(0, ${this.store.size.height})`)
                
                .call(d3.axisBottom(x).ticks(10).tickFormat(d3.format("")));

            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", this.store.size.width / 2)
                .attr("y", this.store.size.height + this.store.margin.bottom - 3)
                .text("Year");
                var maxValue = d3.max(data, function(d) {
                    var values = Object.values(d);
                    values.shift(); // remove first element "year"
                    return d3.max(values.map(Number));
                });

            console.log(maxValue);


            function getMax(data: any) {
                let maxRow = data.reduce((maxRow: any, currentRow: any) => {
                    let currentRowSum = d3.sum(Object.values(currentRow).map(Number));
                    let maxRowSum = d3.sum(Object.values(maxRow).map(Number));
                    return currentRowSum > maxRowSum ? currentRow : maxRow;
                });
                let maxValue = d3.sum(Object.values(maxRow).map(Number));
                console.log('Maxrow: ', maxValue);
                return maxValue;
            }

            


            const y = d3.scaleLinear()
                .domain([0, getMax(data) * 1.25])
                .range([this.store.size.height, 0]);
            svg.append("g")
                .call(d3.axisLeft(y));

            svg.append("text")
                .attr("text-anchor", "end")
                .attr("x", -this.store.size.height / 2 + this.store.margin.bottom + this.store.margin.top)
                .attr("y", - (this.store.margin.right + 40))
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-90)")
                .text("New Housing Production")

            const color = d3.scaleOrdinal(d3.schemeCategory10)
                .domain(keys)

            const stackedData = d3.stack()
                .keys(keys)
                (data)

            svg
                .selectAll("mylayers")
                
                .data(stackedData)
                .join("path")
                .style("fill", function (d) { return color(d.key); })
                
                .attr("d", d3.area()
                    .x((d: any, i: any) => x(d.data.year))
                    .y0((d: any) => y(d[0]))
                    .y1((d: any) => y(d[1]))
                )
                // .attr('height', '90%')
                // .attr('width', '90%')
                // .attr("transform", `translate(${this.store.margin.left}, ${-this.store.margin.bottom})`);


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
    width: 100%
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