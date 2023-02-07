
<script lang="ts">
import * as d3 from "d3";
import { debounce, isEmpty } from 'lodash';
import { Point } from '../types';
import { mapState, storeToRefs } from 'pinia';
import { useHousingStore } from '../stores/housingStore';
import { useCitiesStore } from '../stores/citiesStore'
import { useMapStore } from '../stores/mapStore'
import { useYearStore } from '../stores/yearStore'
import { server } from '../helper';
import { getColors } from "../helpers/colors";
interface ScatterPoint extends Point {
    cluster: string;
}
/* The new major things from ExampleWithLegend.vue
1) Add a dropdown menu to switch between different DR techniques, the changes are mostly in the template
2) Using a store from './dashboard/stores/exampleStore'
3) Composition API rather than Option API (just used a little bit)
*/
// For importing a store. See how it's set up in ./dashboard/stores/ and ./dashboard/main.ts
import { mapState, storeToRefs } from 'pinia';
import { useExampleStore } from '../stores/exampleStore';
import * as fs from 'fs';
import * as fspath from 'path';
import { select, event } from 'd3';
import { json } from 'd3-fetch';
import { geoAlbersUsa, geoPath } from 'd3-geo';
import { zoom } from 'd3-zoom';
import { feature, mesh } from 'topojson-client';
import * as topojson from 'topojson';
import { getCurrentYear } from "../helpers/animate";
export default {
    setup() {
        const store = useHousingStore();
        const citiesStore = useCitiesStore();
        const { resize } = storeToRefs(store);
        const mapStore = useMapStore();
        const yearStore = useYearStore();
        return {
            store,
            citiesStore,
            resize,
            mapStore,
            yearStore
        }
    },
    computed: {
        ...mapState(useHousingStore, ['selectedMethod']),
        ...mapState(useMapStore, []),
        ...mapState(useCitiesStore, ['citiesData']),
        ...mapState(useYearStore, [])
    },
    async created() {
        this.store.fetchHousing(this.selectedMethod);
        await this.mapStore.fetchMap();
        this.citiesStore.fetchCities();
        this.yearStore.setYear(1990);
    },
    methods: {
        onResize() {
            let target = this.$refs.mapContainer as HTMLElement
            if (target === undefined || target === null) return;
            this.citiesStore.size = { width: target.clientWidth, height: target.clientHeight };
        },
        initChart() {

            // console.log('curyear', this.yearStore.year);
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
            if (!this.citiesData.cities) return false
            if (!this.mapStore.map.objects) return false
            let cityData = JSON.parse(JSON.stringify(this.citiesStore.citiesData))

            if (cityData.cities) {
                cityData.cities.sort((b, a) => b.totalproduction - a.totalproduction);
            }
            let housingData: any[] = d3.csvParse(this.store.housing);
            let keys: any[] | Iterable<string> = [];
            if (cityData.cities && Array.isArray(cityData.cities)) {
                cityData.cities.forEach((city: any) => {
                    if (!keys.includes(city.county)) {
                        keys.push(city.county);
                    }
                });
            } else {
                console.error("Cities must be defined and be an array.");
            }
            let radius = d3.scaleSqrt([0, d3.max(JSON.parse(JSON.stringify(this.citiesStore.citiesData.cities)), d => {
                return d.totalproduction
            })], [0, 10 * Math.SQRT2])
                .range([2, 5])
            let cd = JSON.parse(JSON.stringify(this.citiesStore.citiesData.cities));
            let max = 0;
            for (let city of cd) {
                let cur = city.totalproduction;
                if (cur > max) {
                    max = cur;
                }
            }
            const color = getColors(keys);
            const makeMarkers = (cityData: any, housingData: any[]) => {
                let markers = [];
                for (let city of cityData) {
                    // if (city.year !== "2005") {
                    // }
                    // else {
                    let marker = {
                        long: city.longitude,
                        lat: city.latitude,
                        color: color(city.county),
                        r: radius(city.totalproduction),
                        opacity: 0.8,
                        county: city.county,
                        city: city.city,
                        totalproduction: city.totalproduction,
                        year: city.year
                        // r: housingData[0][city.county] / 500
                    }
                    markers.push(marker);
                    // }

                }
                return markers;
            }
            const markers = makeMarkers(cityData.cities, housingData);
            // if (!this.citiesData.cities) return false
            // if (!this.mapStore.map.objects) return false
            //US
            let data = JSON.parse(JSON.stringify(this.mapStore.map));
            let zoom = d3.zoom()
                .scaleExtent([1, 8])
                // .translateExtent([[-500, -300], [1500, 1000]])
                .on("zoom", e => {
                    zoomed(e, this.citiesStore.size.width, this.citiesStore.size.height)
                }
                );
            // The svg
            let svg = d3.select("#map-svg")
                // .attr('width', this.store.size.width + this.store.margin.left + this.store.margin.right + 150)
                .attr('height', this.citiesStore.size.height )
                // .attr("transform", `translate(${this.citiesStore.margin.right / 2}, ${this.citiesStore.margin.top})`)
                .append("g")
                
                .attr("transform", `translate(${this.citiesStore.margin.right / 2}, ${this.citiesStore.margin.top})`)
                .attr("viewBox", [0, 0, this.citiesStore.size.width, this.citiesStore.size.height])
                .attr("transform", `translate(${this.citiesStore.margin.right / 2}, ${this.citiesStore.margin.top})`)

            
            
            // .on("click", reset(this.citiesStore.size.width, this.citiesStore.size.height));
            //                 const radiusScale = d3.scaleSqrt()
            //   .domain([d3.min(markers, d => d.r), d3.max(markers, d => d.r)])
            //   .range([5, 20]);


            var g = svg
                .append('g')

                // .attr('width', this.store.size.width + this.store.margin.left + this.store.margin.right + 150)
                // .attr('height', this.store.size.height + this.store.margin.top + this.store.margin.bottom)
                // .attr("clip-path", "url(#clip)")
                // .attr('width', 10)
                // .attr('height', 10)
                ;

                svg.append('rect')
                .attr('width', this.citiesStore.size.width)
                .attr('height', 50)
                .style('fill', 'white')
                .style('stroke', 'black')
                .style('opacity', 1)
                .attr('transform', `translate(${-this.citiesStore.margin.left}, ${-65})`);
            svg.append("text")
                .attr("text-anchor", "end")
                .attr("font-size", "24px")
                .attr("font-weight", "bold")
                .attr("x", (this.citiesStore.size.width + this.citiesStore.margin.left) / 2)
                
                .attr("y",-25)
                .text("Housing Production by City");

                
            const center = [122.4194, 37.7749];  // longitude and latitude of Bay Area center
            const projection = d3.geoAlbers()
                .rotate([center[0], 0, 0])
                .center([0, center[1]])
                .scale(12000)
                .translate([this.citiesStore.size.width / 2, this.citiesStore.size.height / 2]);
            // const pathGenerator = d3.geoPath().projection(projection);
            const path = d3.geoPath()
            path.projection(projection)
            // US
            // Filling the map
            const states = g.append("g")
                .attr("fill", "#EEE")
                .attr("cursor", "pointer")
                .selectAll("path")
                .data(topojson.feature(data, data.objects.states).features)
                .join("path")
                .attr("d", path)

            // .on("click", (event, d)  => { 
            //     clicked(event, d, this.citiesStore.size.width, this.citiesStore.size.height)
            // });;
            const counties = g.append("g")
                .attr("fill", "#EEE")
                .attr("cursor", "pointer")
                .selectAll("path")
                .data(topojson.feature(data, data.objects.counties).features)
                .join("path")
                .attr("d", path)
                .on("click", (event, d) => {
                    clicked(event, d, this.citiesStore.size.width, this.citiesStore.size.height)
                });;
            // const something = g.append("g")
            // .attr("fill", "#EEE")
            // .attr("cursor", "pointer")
            // .selectAll("path")
            // .data(topojson.feature(data, data.objects.).features)
            // .join("path")
            // .attr("d", path)


            // Filling the map
            // const other = g.append("g")
            //     .attr("fill", "#EEE")
            //     .attr("cursor", "pointer")
            //     .selectAll("path")
            //     .data(topojson.feature(data, data.objects.).features)
            //     .join("path")
            //     .on("click", (event, d) => {
            //         clicked(event, d, this.citiesStore.size.width, this.citiesStore.size.height)
            //     })
            //     .attr("d", path);
            //
            // const counties = topojson.mesh(data, data.objects.counties);
            const regions = g.append("path")
                .attr("fill", "none")
                .attr("stroke", "grey")
                .attr("stroke-linejoin", "round")
                .attr("d", path(topojson.mesh(data, data.objects.counties)))
            const latitude = 37.7749;
            const longitude = -122.4194;
            const markers2 = [
                { long: -122.4194, lat: 37.7749 }, // SF
            ];
            const bubbles = g.selectAll('circle')
                .data(markers)
                .enter()
                .append('circle')
                .attr("d", d => d3.geoPath().projection(projection)
                )
                .attr("class", d => {
                    return "bubble " + d.county.replaceAll(' ', '')
                })
                .attr("cx", d => {
                    if (projection([d.long, d.lat])) {
                        return projection([d.long, d.lat])[0]
                    }
                    else {
                    }
                })
                .attr("cy", d => {
                    if (projection([d.long, d.lat])) {
                        return projection([d.long, d.lat])[1]
                    }
                })
                .attr('r', d => {
                    if (parseInt(d.year) === this.yearStore.year) {
                        if (d.r > 0) {
                            return d.r;
                        }
                        else {
                            return 0;
                        }
                    }
                })
                .attr('fill', d => d.color)
                .attr('stroke', "black")
                // .attr('stroke-width', .5)
                .attr('opacity', d => d.opacity)
                .on("mouseover", function (event, d) {
                    tooltip.html(
                        `<div>City: ${d.city}</div>`
                    )
                        .style('visibility', 'visible');
                })
                .on('mousemove', function (event, d) {
                    tooltip
                        .style('top', (event.pageY - 10) + 'px')
                        .style('left', (event.pageX + 10) + 'px');
                })
                .on("mouseleave", function (event, d) {
                    tooltip.html(``).style('visibility', 'hidden');
                })
                .on("click", (event, d) => {
                    BubbleClicked(event, d, this.citiesStore.size.width, this.citiesStore.size.height)
                })
            // let startYear = 1990;
            // let endYear = 2018;
            // let currentYear = startYear;
            //     d3.interval(() => {
            //     bubbles.transition()
            //         .duration(10)
            //         .attr('r', d => {
            //             if (parseInt(d.year) === parseInt(currentYear)) {
            //             if(d.city === 'San Francisco' && d.county === 'San Francisco County') {
            //                 console.log('d.r: ', d.r)
            //                 console.log('d.year:', d.year)
            //                 console.log('currentYear: ', currentYear)
            //             }
            //             if (d.r > 0) {
            //                 return d.r
            //             }
            //             else {
            //                 return 0;
            //             }
            //             }
            //         });
            //         currentYear = (currentYear + 1) % (endYear - startYear + 1) + startYear;
            //     }, 5000);
            let startYear = 1990;
            let endYear = 2018;
            let currentYear = startYear;
            console.log('currentYear: ', currentYear)
            let productionData = markers.filter(d => parseInt(d.year) === parseInt(currentYear)).map(d => {
                return {
                    long: d.long,
                    lat: d.lat,
                    color: d.color,
                    r: d.r,
                    opacity: d.opacity,
                    county: d.county,
                    city: d.city,
                    totalproduction: d.totalproduction,
                    year: d.year
                };
            });
            // d3.interval(() => {
            function animate() {
                productionData = markers.filter(d => parseInt(d.year) === parseInt(currentYear)).map(d => {
                    return {
                        long: d.long,
                        lat: d.lat,
                        color: d.color,
                        r: d.r,
                        opacity: d.opacity,
                        county: d.county,
                        city: d.city,
                        totalproduction: d.totalproduction,
                        year: d.year
                    };
                });
                bubbles.data(productionData, d => d.city)
                    .transition()
                    .duration(1000)
                    .ease(d3.easeLinear)
                    .attr('r', d => {
                        if (d.city === 'San Francisco' && d.county === 'San Francisco County') {

                        }
                        if (d.r > 0) {
                            return d.r
                        }
                        else {
                            return 0;
                        }
                    })


                if (currentYear === endYear) {
                    currentYear = startYear;
                }
                else {
                    currentYear = currentYear + 1;
                }
                if (currentYear <= endYear) {
                    d3.timeout(animate, 1000);
                }
            }
            // animate();
            function BubbleClicked(event, d, width, height) {
                // event.target.attr("z-index", "-1");
                let coords = projection([event.layerX, event.layerY]);
                let selectedColor = d.color;
                let selectedCircles = d3.selectAll('circle')
                    .filter(circle => circle['color'] === selectedColor);
                const longs = selectedCircles._groups[0].map(d => d.__data__.long);
                const lats = selectedCircles._groups[0].map(d => d.__data__.lat);

                // const longitudes = selectedCircles.data().map(d => d.long);
                // const latitudes = selectedCircles.data().map(d => d.lat);
                // Need to calculate this right so it's like xx and yy
                const x0 = d3.min(longs);
                const x1 = d3.max(longs);
                const y0 = d3.min(lats);
                const y1 = d3.max(lats);

                // let mids = ([findMiddle(x0, x1), findMiddle(y0,y1)])
                function findAverage(arr) {
                    let sum = 0;
                    for (let i = 0; i < arr.length; i++) {
                        sum += arr[i];
                    }
                    return sum / arr.length;
                }
                function findAveragex(arr) {
                    let sum = 0;
                    for (let i = 0; i < arr.length; i++) {
                        if (arr[i] > 0
                        ) {
                            sum += -arr[i];
                        }
                        sum += arr[i];
                    }
                    return sum / arr.length;
                }
                let medx = findAveragex(longs)
                let medy = findAverage(lats)
                let midx = projection([medx, medy])[0]
                let midy = projection([medx, medy])[1]
                function findMiddle(a, b) {
                    return (a + b) / 2;
                }
                let lat = selectedCircles._groups[0][0].__data__.lat
                let long = selectedCircles._groups[0][0].__data__.long
                let xx = projection([d.long, d.lat])[0]
                let yy = projection([d.long, d.lat])[1]

                svg.transition().duration(750).call(
                    zoom.transform,
                    d3.zoomIdentity
                        .translate(width / 2, height / 2)
                        .scale(Math.min(8, 1.5 / Math.max((midx) / width, (midy) / height)))
                        .translate(-(midx), -(midy)),
                    d3.pointer(event, svg.node())
                );

            }



            const legendWidth = 150;
            const legendHeight = 200;
            // Create a group for the legend
            const legend = svg.append('g')
                .attr('id', 'legend')
                .attr('background-color', 'white')
                .attr('border', '1px solid black')
                .attr('transform', `translate(${10}, ${this.citiesStore.size.height - legendHeight - 140})`);
            // Add a rectangle with a background color for the legend
            let legendRect = legend.append('rect')
                .attr('width', legendWidth)
                .attr('height', legendHeight)
                .style('fill', 'white')
                .style('stroke', 'black')
                .style('opacity', 0.8)
                .attr('transform', `translate(${-this.citiesStore.margin.left + 50}, 75)`);

            //   .attr('transform', `translate(${10}, ${this.citiesStore.size.height - legendHeight - 10})`);
            let legendRadius = d3.scaleSqrt([0, d3.max(JSON.parse(JSON.stringify(this.citiesStore.citiesData.cities)), d => {
                return d.totalproduction
            })], [0, Math.SQRT2])
                .range([2, 15])
            // The scale you use for bubble size
            const size = legendRadius
                .domain([1, 1000])  // What's in the data, let's say it is percentage
                .range([1, 100])  // Size in pixel
            // Add legend: circles
            const valuesToShow = [10, 50, radius(1000)]
            let legendData = [radius(500), radius(2500), radius(5000)]
            let maxBubbleSize = legendData[1];
            let bubbleSizeScale = radius
                //   .domain([0, d3.max(legendData)])
                .range([0, 5000])
            const xCircle = 230
            const xLabel = 300
            const yCircle = 330


            
            legend
                .selectAll("legend")
                .data(legendData)
                .join("circle")
                .attr("cx", xCircle)
                .attr("cy", (d, i) => {
                    return yCircle - d
                    // yCircle - (d / (i))
                })
                .attr("r", d => {
                    return maxBubbleSize * (d / maxBubbleSize)
                })
                //   .attr('transform', `translate(${-175}, 100)`)
                .attr('transform', `translate(${-240}, -60)`)
                .style("fill", "none")
                .attr("stroke", "black")
            // Add legend: segments
            legend
                .selectAll("legend")
                .data(legendData)
                .join("line")
                .attr('x1', d => xCircle + d)
                .attr('x2', xLabel)
                .attr('y1', d => yCircle - d)
                .attr('y2', d => yCircle - d)
                .attr('stroke', 'black')

                .attr('transform', `translate(${-240}, -60)`)
                //   .attr('transform', `translate(${-175}, 100)`)
                .style('stroke-dasharray', ('2,2'))
            // Add legend: labels
            legend
                .selectAll("legend")
                .data([500, 2500, 5000])
                .join("text")
                .attr('x', xLabel)
                .attr('y', d => yCircle - size(d / 50))
                .text(d => d)
                .style("font-size", 10)

                .attr('transform', `translate(${-240}, -60)`)
                //   .attr('transform', `translate(${-175}, 100)`)
                .attr('alignment-baseline', 'middle')


                legend.append("text")
                .attr("text-anchor", "end")
                .attr("font-size", "12px")
                .attr("font-weight", "bold")
                .attr("x", 0)
                
                .attr('transform', `translate(${80}, 225)`)
                .attr("y",-25)
                .text("Number of Units Built");

            svg.call(zoom);
            function reset(states, width, height) {
                if (typeof states !== 'Object') {
                    return;
                }
                else {
                    states.transition().style("fill", null);
                    svg.transition().duration(750).call(
                        zoom.transform,
                        d3.zoomIdentity,
                        d3.zoomTransform(svg.node()).invert([width / 2, height / 2])
                    );
                }
            }
            function clicked(event, d, width, height) {
                const [[x0, y0], [x1, y1]] = path.bounds(d);
                event.stopPropagation();
                states.transition().style("fill", null);
                svg.transition().duration(750).call(
                    zoom.transform,
                    d3.zoomIdentity
                        .translate(width / 2, height / 2)
                        .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
                        .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
                    d3.pointer(event, svg.node())
                );
            }
            function zoomed(event) {
                const { transform } = event;
                g.attr("transform", transform);
                g.attr("stroke-width", 1 / transform.k);

                bubbles.attr('r', d => {
                    if (parseInt(d.year) === this.yearStore.year) {
                        if (d.r > 0) {
                            return d.r / transform.k
                        }
                        else {
                            return 0;
                        }
                    }
                });
                // g.attr("path", path * transform.k);
            }
        },
        initLegend() {
        },
        rerender() {
            d3.select('#map-svg').selectAll('*').remove() // Clean all the elements in the chart
            this.initChart()
            this.initLegend()
        }
    },
    async mounted() {
        // let data = d3.json(`${server}/fetchCitiesWithCoords`)
        // this.data = data;
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
        'yearStore.year'(data) { // when data changes
            // if (!isEmpty(data)) {
            this.rerender()
            // }
        },
        'store.housing'(data) { // when data changes
            if (!isEmpty(data)) {
                this.rerender()
            }
        },
        'citiesStore.citiesData'(data) { // when data changes
            if (!isEmpty(data)) {
                this.rerender()
            }
        },
        'mapStore.map'(data) { // when data changes
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

<!-- We only use vanilla widgets here, you can use the equivalent components from the UI library -->
<!-- Helpful References: https://vuejs.org/guide/essentials/class-and-style.html#binding-html-classes -->
<template>
    <!-- <div class="viz-container d-flex justify-end"> -->

    <!-- <div ref="parallelContainer" class="chart-container outer d-flex"> -->
    <div id="chartcontainer" class="chart-container" ref="mapContainer">
        <svg id="map-svg">
        </svg>
    </div>
    <!-- </div> -->
</template>

<style scoped>
.viz-container {
    height: 100%;
    flex-direction: row;
    flex-wrap: nowrap;
}

.chart-container {
    height: 100%;
    width: calc(100% - 6rem);
    /* border: 1px solid black; */
    /* adds a 1px black border */
    position: relative;
    overflow: hidden;
}

#map-svg {
    /* height: 100%; */
    width: calc(100% - 3.9rem);
    border: 1px solid black;
    background-color: rgb(200, 218, 240);
}

#scatter-control-container {
    width: 6rem;
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




// Brush - bisect
// Hover over and move the map
// Click to zoom
// Plot title
// Title legend