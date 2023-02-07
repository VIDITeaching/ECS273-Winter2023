<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';
import { swatches } from "@d3/color-legend"

import { Point, ComponentSize, Margin } from '../types';
interface ScatterPoint extends Point{
    cluster: string;
}
interface DryBean {
    Area: number;
    // Perimeter: number;
    // MajorAxisLength: number;
    // MinorAxisLength: number;
    AspectRation: number;
    // Eccentricity: number;
    ConvexArea: number;
    // EquivDiameter: number;
    // Extent: number;
    // Solidity: number;
    // roundness: number;
    Compactness: number;
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

// =================================================================
import { mapState, storeToRefs } from 'pinia'; 
import { useExampleStore } from '../stores/exampleStore';
// =================================================================

export default {
    // =================================================================    
    //data() {
    //    return {
    //        points: [] as ScatterPoint[],
    //        clusters: [] as string[],
    //        size: { width: 0, height: 0 } as ComponentSize,
    //        margin: {left: 60, right: 20, top: 20, bottom: 60} as Margin,
    //    }
    //},
    setup() { // Composition API syntax
        const store = useExampleStore()
        // Alternative expression from computed
        const { resize } = storeToRefs(store);
        return {
            store, // Return store as the local state, but when you update the property value, the store is also updated.
            resize,
        }
    },
    // =================================================================            
    computed: {
        // ===================================================
        //rerender() {
        //    return (!isEmpty(this.points))  && this.size
        //}
        ...mapState(useExampleStore, ['selectedMethod']) // Traditional way to map the store state to the local state        
    },
    created() {
    // =================================================================    
    //    axios.get(`${server}/fetchExample`)
    //        .then(resp => {
    //            this.points = resp.data.data;
    //            this.clusters = resp.data.clusters;
    //            return true;
    //        })
    //        .catch(error => console.log(error));
        this.store.fetchExample(this.selectedMethod);        // console.log(this.store);
    // =================================================================    
    },
    methods: {
        onResize() {
            let target = this.$refs.scatterContainer as HTMLElement
            if (target === undefined || target === null) return;
            // =================================================================    
            // this.size = { width: target.clientWidth, height: target.clientHeight };
            this.store.size = { width: target.clientWidth - this.store.margin.left - this.store.margin.right, 
                                height: target.clientHeight - this.store.margin.top - this.store.margin.bottom };

            // =================================================================    
        },
        initChart() {
            if(this.store.selectedMethod == 'scatter'){
                const marginWhole = {top: 20, right: 60, bottom: 20, left: 20},
                        sizeWhole = 640 - marginWhole.left - marginWhole.right

                let matrix_columns = ["Area", "AspectRation", "Compactness", "ConvexArea", "Class"];
                const domain_org: string[] = this.store.clusters;
                // const domains = d3.csvParse(domain_org.join(','));
                // let domains = this.store.columns;
                // console.log(domains)
                // console.log(domains)
                
                let domains = d3.csvParse(this.store.columns.join(','));
                domains = domains['columns'].filter(function(d) { return d != "Class" })
                // const domains: string[] = this.store.clusters;
                // const filepath = this.store.filepath
                // const filepath = '/public/dry_bean_short.csv'
                // console.log('domains')

                const svg = d3.select('#scatter-bean-svg')
                
                svg.append('svg')
                        .attr('width', sizeWhole + marginWhole.left + marginWhole.right)
                        .attr('height', sizeWhole + marginWhole.top + marginWhole.bottom )
                    .append('g')
                        .attr('transform', `translate(${marginWhole.left},${marginWhole.top})`);

                // d3.csv(filepath).then( function(data) {
                const data = this.store.bean_data;

                const allVar = domains
                const numVar = allVar.length

                let mar = 20
                let size = sizeWhole / numVar

                  // Create a scale: gives the position of each pair each variable
                const position = d3.scalePoint()
                    .domain(allVar)
                    .range([0, sizeWhole-size])

                  // Color scale: give me a specie name, I return a color
                const color = d3.scaleOrdinal()
                    .domain(domains)
                    .range(d3.schemeTableau10)

              for (let i in allVar){
                    for (let j in allVar){

                      // Get current variable name
                    const var1 = allVar[i]
                    const var2 = allVar[j]

                      // If var1 == var2 i'm on the diagonal, I skip that
                    if (var1 === var2) { continue; }

                      // Add X Scale of each graph
                    let xextent = d3.extent(data, function(d) { return +d[var1] })
                    const x = d3.scaleLinear()
                        .domain(xextent).nice()
                        .range([ 0, size-2*mar ]);

                      // Add Y Scale of each graph
                    let yextent = d3.extent(data, function(d) { return +d[var2] })
                    const y = d3.scaleLinear()
                        .domain(yextent).nice()
                        .range([ size-2*mar, 0 ]);

                      // Add a 'g' at the right position
                    const tmp = svg
                        .append('g')
                        .attr("transform", `translate(${position(var1)+mar},${position(var2)+mar})`);

                      // Add X and Y axis in tmp
                    tmp.append("g")
                        .attr("transform", `translate(0,${size-mar*2})`)
                        .call(d3.axisBottom(x).ticks(3));

                    tmp.append("g")
                        .call(d3.axisLeft(y).ticks(3));

                      // Add circle
                    tmp.selectAll("myCircles")
                        .data(data)
                        .join("circle")
                          .attr("cx", function(d){ return x(+d[var1]) })
                          .attr("cy", function(d){ return y(+d[var2]) })
                          .attr("r", 1)
                          .attr("fill", function(d){ return color(d.Class)})
                          .attr("fill-opacity", 0.2)
                    }
                }

                for (let i in allVar){
                    for (let j in allVar){
                        // If var1 == var2 i'm on the diagonal, otherwisee I skip
                        if (i != j) { continue; }
                        // Add text
                        const var1 = allVar[i]
                        const var2 = allVar[j]
                    
                    svg.append('g')
                        .attr("transform", `translate(${position(var1)},${position(var2)})`)
                        .append('text')
                          .attr("x", size/2)
                          .attr("y", size/2)
                          .text(var1)
                          .attr("text-anchor", "middle")
                    }
                }
                // })
                const title = svg.append('g')
                    .append('text') // adding the text
                    .attr('transform', `translate(${sizeWhole / 2}, ${sizeWhole+marginWhole.bottom})`)
                    .attr('dy', '0.5rem') // relative distance from the indicated coordinates.
                    .style('text-anchor', 'middle')
                    .style("font", "bold 15px sans-serif")
                    .text('Dry bean - Scatter plot matrix') // text content                
            }
            else{
                let chartContainer = d3.select('#scatter-bean-svg')

                chartContainer.append('svg')
                        .attr('width', this.store.size.width - this.store.margin.left - this.store.margin.right)
                        .attr('height', this.store.size.width - this.store.margin.top - this.store.margin.bottom)

                // ==== changed to : points => store =============
                let xExtents = d3.extent(this.store.points.map((d: ScatterPoint) => d.posX as number)) as [number, number]
                let yExtents = d3.extent(this.store.points.map((d: ScatterPoint) => d.posY as number)) as [number, number]

                let xScale = d3.scaleLinear()
                    .range([this.store.margin.left, this.store.size.width - this.store.margin.right])
                    .domain(xExtents)

                let yScale = d3.scaleLinear()
                    .range([this.store.size.height - this.store.margin.bottom, this.store.margin.top])
                    .domain(yExtents)

                // let clusters: string[] = this.clusters.map((cluster: string, idx: number) => String(idx))
                let clusters: string[] = this.store.clusters
                let colorScale = d3.scaleOrdinal().domain(clusters).range(d3.schemeTableau10) // d3.schemeTableau10: string[]

                const points = chartContainer.append('g')
                    .selectAll('circle')
                    .data<ScatterPoint>(this.store.points)
                    .join('circle')
                    .attr('cx', (d: ScatterPoint) => xScale(d.posX))
                    .attr('cy', (d: ScatterPoint) => yScale(d.posY))
                    .attr('r', 2)
                    .style('fill', (d: ScatterPoint) => colorScale(String(d.cluster)) as string)
                    .style('opacity', .7)

                const title = chartContainer.append('g')
                    .append('text')
                    .attr('transform', `translate(${this.store.size.width / 2}, ${this.store.size.height + this.store.margin.top})`)
                    .attr('dy', '0.5rem')
                    .style("font", "bold 15px sans-serif")
                    .style('text-anchor', 'middle')
                    .style('font-weight', 'bold')
                    .text(`Drybean Dataset ${this.selectedMethod} Projection`)

                const xAxis = chartContainer.append('g')
                    .attr('transform', `translate(0, ${this.store.size.height - this.store.margin.bottom})`)
                    .call(d3.axisBottom(xScale))

                const yAxis = chartContainer.append('g')
                    .attr('transform', `translate(${this.store.margin.left}, 0)`)
                    .call(d3.axisLeft(yScale))

                const yLabel = chartContainer.append('g')
                    .attr('transform', `translate(${this.store.margin.left}, ${this.store.size.height/2 + this.store.margin.top}) rotate(-90)`)
                    .style("font", "bold 12px sans-serif")
                    .append('text')
                    .text('Dim_2')

                const xLabel = chartContainer.append('g')
                    .attr('transform', `translate(${this.store.size.width/2}, ${this.store.size.height + this.store.margin.top/7})`)
                    .style("font", "bold 12px sans-serif")
                    .append('text')
                    .text('Dim_1')
            }
    
        },
        initLegend() {
            let legendContainer = d3.select('#scatter-legend-svg')

            // let clusterLabels: string[] = this.clusters.map((cluster: string, idx: number) => `Cultivar ${idx+1}`)
            let clusterLabels: string[] = this.store.clusters
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
        },
        rerender() {
            d3.select('#scatter-bean-svg').selectAll('*').remove() // Clean all the elements in the chart
            d3.select('#scatter-legend-svg').selectAll('*').remove()
            this.initChart()
            this.initLegend()
        }
    },
    watch: { // updated because a legend is added.
        // =========================================================================
        //rerender(newSize) {
        //    if (!isEmpty(newSize)) {
        //        d3.select('#scatter-bean-svg').selectAll('*').remove()
        //        d3.select('#scatter-legend-svg').selectAll('*').remove()
        //        this.initChart()
        //        this.initLegend()
        //    }
        //}
        // =========================================================================        
        resize(newSize) { // when window resizes
            if ((newSize.width !== 0) && (newSize.height !== 0)) {
                this.rerender()
            }
        },
        'store.points'(newPoints) { // when data changes
            if (!isEmpty(newPoints)) {
                this.rerender()
            }
        },
        selectedMethod(newMethod) { // function triggered when a different method is selected via dropdown menu
            this.store.fetchExample(newMethod)
            this.rerender()
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
    <div class="viz-container d-flex justify-end">
        <div class="chart-container d-flex" ref="scatterContainer">
            <svg id="scatter-bean-svg" width="100%" height="100%">
            </svg>
        </div>
        <div id="scatter-control-container" class="d-flex">
            <div class="d-flex mb-4">
                <label :style="{ fontSize: '0.7rem'}"> Select Method:
                    <select class="method-select" v-model="store.selectedMethod">
                        <option v-for="method in store.methods" :value="method" 
                            :selected="(method === store.selectedMethod)? true : false">{{method}}</option>
                    </select>
                </label>
            </div>
            <svg id="scatter-legend-svg" width="100%" height="80%">
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
#scatter-control-container{
    width: 6rem;
    flex-direction: column;
}
.method-select{
    outline: solid;
    outline-width: 1px;
    outline-color: lightgray;
    border-radius: 2px;
    width: 100%;
    padding: 2px 5px;
}
#scatter-legend-container{
    width: 5rem;
}
</style>