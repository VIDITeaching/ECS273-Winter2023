<script lang="ts">
import * as d3 from "d3";

import world from '../assets/countries-50m.json';
import * as topojson from "topojson-client"

import { useTerrorismDataStore } from '../stores/terrorismDataStore';


const width = 700;
const height = 400;

// const projection = d3.geoEqualEarth();
let projection = d3.geoMercator()
    .scale(width / 2.5 / Math.PI)
    .translate([width / 2, height / 2]);

let k = 1;


export default {
    setup() { // Composition API syntax
        const store = useTerrorismDataStore()
        return {
            store, // Return store as the local state, but when you update the property value, the store is also updated.
        }
    },
    mounted() {
        console.log("mounted");
        this.initChart();

    },
    beforeDestroy() {
    },
    created() {
        //this.updateChart();
    },
    methods: {
        initChart() {
            console.log("initChart");

            let context = this; // for avoidng this context problems

            // console.log(world)
            // console.log("Init Chart")

            const countries = topojson.feature(world, world.objects.countries)
            const countrymesh = topojson.mesh(world, world.objects.countries, (a, b) => a !== b)

            // Construct a path generator.
            const path = d3.geoPath(projection);

            let zoomed = function (event) {
                k = event.transform.k;
                g.style("stroke-width", 1.5 / k + "px");
                g.attr("transform", event.transform); // updated for d3 v4
                g.selectAll(".dot").attr("r", 4 / k + "px");
            }
            let zoom = d3.zoom().on("zoom", zoomed);

            let stopped = function (event) {
                if (event.defaultPrevented) event.stopPropagation();
            }
            let reset = function () {
                active.classed("active", false);
                active = d3.select(null);

                svg.transition()
                    .duration(750)
                    // .call( zoom.transform, d3.zoomIdentity.translate(0, 0).scale(1) ); // not in d3 v4
                    .call(zoom.transform, d3.zoomIdentity); // updated for d3 v4

                context.store.selectedIncident = null;
                context.store.countrieFilter = null;
                context.store.filterData();

            }

            var active = d3.select(null);

            let svg = d3.select("#overviewChart")
                .attr("width", width)
                .attr("height", height)
                .on("click", stopped, true);
            ;

            svg.append("rect")
                .attr("class", "background")
                .attr("width", "100%")
                .attr("height", "100%")
                .attr("fill", "#e6e6e6")
                ;


            let clickedCountrie = function (event, d) {

                if (active.node() === this)
                    return reset();

                active.classed("active", false);
                active = d3.select(this).classed("active", true);

                var bounds = path.bounds(d),
                    dx = bounds[1][0] - bounds[0][0],
                    dy = bounds[1][1] - bounds[0][1],
                    x = (bounds[0][0] + bounds[1][0]) / 2,
                    y = (bounds[0][1] + bounds[1][1]) / 2,
                    scale = Math.max(1, Math.min(8, 0.9 / Math.max(dx / width, dy / height))),
                    translate = [width / 2 - scale * x, height / 2 - scale * y];

                svg.transition()
                    .duration(750)
                    .call(zoom.transform, d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale));

                context.store.countrieFilter = d.properties.name;
                context.store.selectedIncident = null;
                context.store.filterData();

            }


            let mouseOver = function (event, d) {
                // console.log(d.properties.name);
                d3.select("#filter_country")
                    .text("Country: " + d.properties.name);


                d3.selectAll(".Country")
                    .transition()
                    .duration(200)
                    .style("opacity", .8)
                    .style("stroke", "white");

                d3.select(this)
                    .transition()
                    .duration(200)
                    .style("opacity", 1)
                    .style("stroke", "black")
            }

            let mouseLeave = function (event, d) {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .style("opacity", .8)
                    .style("stroke", "white");

            }

            let g = svg.append("g")
                .attr("id", "mapContainer");

            svg.call(zoom); // delete this line to disable free zooming


            g.selectAll("path")
                .data(countries.features)
                .join("path")
                .attr("fill", "grey")
                .style("stroke", "white")
                .style("opacity", .8)
                .attr("class", "Country")
                .attr("d", path)
                .on("mouseover", mouseOver)
                .on("mouseleave", mouseLeave)
                .on("click", clickedCountrie);

            let legend = svg.append("g")
                .attr("id", "legendContainer");

            legend.append("text")
                .attr("id", "legendKillMin")
                .text("0")
                .attr("x", 12)
                .attr("y", 320)
                .style("font-size", 12);

            legend.append("text")
                .attr("id", "legendKillMax")
                .text("100")
                .attr("x", 12)
                .attr("y", 45)
                .style("font-size", 12);


            g.append("g")
                .attr("id", "dotsContainer");
        },
        updateChart() {

            console.log("Update Chart Overview " + this.store.terrorismDataFiltered.length)

            // console.log("Drawing: " + this.store.terrorismData.length);

            // inspired by: https://observablehq.com/@mbostock/walmarts-growth
            // and: https://observablehq.com/@d3/world-choropleth

            let svg = d3.select("#overviewChart");
            const g = svg.select("#dotsContainer");

            // console.log(this.store.terrorismData)

            // LEGEND
            const max = d3.max(this.store.terrorismDataFiltered, (d) => {
                let nkill = parseInt(d.nkill) || 0;
                return nkill;
            });

            svg.select("#legendContainer")
                .select("#legendKillMax")
                .text("Killed: " + max);

            let interpolator = d3.interpolate("#FFFFFF", "#B22222");
            let colorScale = d3.scaleSequential(interpolator)
                .domain([0, max]);

            let data = Array.from(Array(100).keys());
            let cScale = d3.scaleSequential()
                .interpolator(interpolator)
                .domain([0, 99]);

            let xScale = d3.scaleLinear()
                .domain([99, 0])
                .range([0, 250]);

            svg.select("#legendContainer")
                .selectAll("rect")
                .data(data)
                .join("rect")
                .attr("x", 10)
                .attr("y", (d) => Math.floor(xScale(d)) + 50)
                .attr("height", (d) => {
                    if (d == 99) {
                        return 6;
                    }
                    return - Math.floor(xScale(d + 1)) + Math.floor(xScale(d)) + 2;
                })
                .attr("width", 20)
                .attr("fill", (d) => cScale(d));

            const context = this; //avoid this problems

            // console.log(this.store.terrorismDataFiltered)

            const dot = g.selectAll("circle")
                .data(this.store.terrorismDataFiltered)
                .join(
                    enter => enter
                        .append("circle")
                        .attr("transform", d => `translate(${projection([d.longitude, d.latitude])})`)
                        .attr("r", d => {
                            return 4 / k + "px";
                        })
                        .attr("class", "dot")
                        .attr("fill", d => {
                            if (this.store.selectedIncident && d.eventid == this.store.selectedIncident.eventid) {
                                return "blue"
                            }
                            return colorScale(d.nkill)
                        })
                        .style("stroke", d => {
                            if (this.store.selectedIncident && d.eventid == this.store.selectedIncident.eventid) {
                                return "white"
                            }
                            return "black";
                        })
                        .style("opacity", d => {
                            if (this.store.selectedIncident && d.eventid == this.store.selectedIncident.eventid) {
                                return 1
                            }
                            return .6;
                        })
                        .on("click", (event) => {
                            const datum = event.target.__data__;
                            // console.log(datum)
                            this.store.selectedIncident = datum;
                        }),
                    update => update
                        .attr("transform", d => `translate(${projection([d.longitude, d.latitude])})`)
                        .attr("fill", d => {
                            if (this.store.selectedIncident && d.eventid == this.store.selectedIncident.eventid) {
                                return "blue"
                            }
                            return colorScale(d.nkill)
                        })
                        .style("stroke", d => {
                            if (this.store.selectedIncident && d.eventid == this.store.selectedIncident.eventid) {
                                return "white"
                            }
                            return "black";
                        })
                        .style("opacity", d => {
                            if (this.store.selectedIncident && d.eventid == this.store.selectedIncident.eventid) {
                                return 1
                            }
                            return .6;
                        }),
                    exit => exit
                        .remove()
                )
        },
    },
    watch: { // updated because a legend is added.
        // 'store.terrorismData'(newTerrorismData) { // when data changes
        //     this.updateChart();
        // },
        'store.terrorismDataFiltered'(newTerrorismData) { // when data changes
            this.updateChart();
        },
        'store.selectedIncident'(newSelectedIncident) { // when data changes
            this.updateChart();
        },
    },
}
</script>

<!-- We use flex to arrange the layout-->
<template>
      <h3 class="ma-2"> Terrorism Events Map</h3>
    <svg id="overviewChart">
    </svg>
</template>

<!-- How we arrange the two svgs with css-->
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
</style>