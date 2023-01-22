

<script lang="ts">
import * as d3 from "d3";
import { debounce, isEmpty } from 'lodash';
import { Point } from '../types';

import { mapState, storeToRefs } from 'pinia';
import { useHousingStore } from '../stores/housingStore';
import { useCitiesStore } from '../stores/citiesStore'
import { server } from '../helper';
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

export default {
    setup() {
        const store = useHousingStore();
        const citiesStore = useCitiesStore();
        const { resize } = storeToRefs(store);
        const countyCoordinates = {
            "Alameda County": {
                "latitude": 37.668819,
                "longitude": -121.777915
            },
            "Marin County": {
                "latitude": 38.107419,
                "longitude": -122.569709
            },
            "Santa Clara County": {
                "latitude": 37.354130,
                "longitude": -121.955236
            },
            "Napa County": {
                "latitude": 38.297538,
                "longitude": -122.286865
            },
            "Contra Costa County": {
                "latitude": 37.917934,
                "longitude": -121.739659
            },
            "San Mateo County": {
                "latitude": 37.562992,
                "longitude": -122.325525
            },
            "San Francisco County": {
                "latitude": 37.774929,
                "longitude": -122.419416
            },
            "Sonoma County": {
                "latitude": 38.291859,
                "longitude": -122.458036
            },
            "Solano County": {
                "latitude": 38.249358,
                "longitude": -121.939983
            }
        };


        return {
            countyCoordinates,
            store,
            citiesStore,
            resize
        }
    },
    computed: {
        ...mapState(useHousingStore, ['selectedMethod']),

        ...mapState(useCitiesStore, ['citiesData'])
    },

    created() {
        this.store.fetchHousing(this.selectedMethod);

        this.citiesStore.fetchCities();
    },
    methods: {

        onResize() {
            let target = this.$refs.mapContainer as HTMLElement

            if (target === undefined || target === null) return;
            this.citiesStore.size = { width: target.clientWidth, height: target.clientHeight };
        },
        async initChart() {


            // console.log('mesh: ', mesh(us, us.objects.states))
            // Create data for circles:
            // Create data for circles:
            // const markers = [
            //     { long: -122.4194, lat: 37.7749 }, // SF
            // ];


            // Map and projection
            const projection = d3.geoAlbers()
            // .fitWidth(0, this.citiesStore.size.width - 100)
            // .fitHeight(this.citiesStore.margin.bottom, this.citiesStore.size.height - this.citiesStore.margin.top)
                .translate([0, 0])
                // .rotate([90,0])
                .scale(12000)
                // .rotate([0, -40])  // rotate around longitude -120, latitude -40
    .center([-28, 39])
    .parallels([35, -30])
    // .scale(6000)

                // var projection = d3.geoAlbersUsa()
                // .scale(1000)
                // .translate([(this.citiesStore.size.width + this.citiesStore.margin.left + this.citiesStore.margin.right) / 2, (this.citiesStore.size.height + this.citiesStore.margin.top + this.citiesStore.margin.bottom) / 2]);

                // console.log('fetchhouse: ', this.store.housing)

            // console.log('fetchCities: ', this.citiesStore.citiesData)
            let cityData = JSON.parse(JSON.stringify(this.citiesStore.citiesData.cities))
            let housingData: any[] = d3.csvParse(this.store.housing);

            // let cityData: any[] = d3.json(this.citiesStore);
            // console.log('city data: ', cityData);

            const keys = housingData.columns.slice(1);
            console.log('keys: ', keys)
            // Load external data and boot
            // let data = await d3.json("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json")
            let data = await d3.json("https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/CA-06-california-counties.json")
            // .then(function (data) {

                console.log('cities: ', cityData)

            let radius = d3.scaleSqrt([0, d3.max( JSON.parse(JSON.stringify(this.citiesStore.citiesData.cities)), d => {
            return d.totalproduction})], [0, 2 * Math.SQRT2])

            const color = d3.scaleOrdinal(d3.schemeCategory10)
            
                .domain(keys)
                .range(d3.schemeTableau10)

            const makeMarkers = (cityData, housingData) => {
                console.log('cityData: ', cityData)
                let markers = [];
                for (let city of cityData) {
                    if (city.year === "2010") {
                        // console.log(radius(10000))
                        console.log('city: ', cityData)
                            // console.log('city: ', city)
                        let marker = {
                            long: city.longitude,
                            lat: city.latitude,
                            color: color(city.county),
                            r: radius(city.totalproduction)
                            // r: housingData[0][city.county] / 500
                        }

                    markers.push(marker);

                    }
                    
                }
                console.log('markers: ', markers)
                return markers;
            }

            const markers = makeMarkers(cityData, housingData);


            // console.log('housing data: ', housingData)

            
            // The svg
            const svg = d3.select("svg")
                .attr('width', (this.citiesStore.size.width))
                .attr('height', (this.citiesStore.size.height))
                // .append(g)

            var g = svg.append("g");

                
            // Create the geo path generator
            const path = d3.geoPath()
                .projection(projection);

            // Filter data
            // data.features = data.features.filter(d => d.properties.name == "California")
            const counties = topojson.feature(data, data.objects.cb_2015_california_county_20m);

svg.append("path")
  .datum(counties)
  .attr("d", path)
  .attr("class", "county")
  .attr("fill", "none")
      .attr("stroke", "#777")
      .attr("stroke-width", 0.5)
      .attr("stroke-linejoin", "round")
      .attr("d", d3.geoPath()
                    .projection(projection)
                )
    //   .attr("d", d3.geoPath());
            // Draw the map
            // svg
            //     .selectAll("path")
            //     .data(data.features)
            //     .join("path")
            //     .attr("fill", "#b8b8b8")
            //     .attr("d", d3.geoPath()
            //         .projection(projection)
            //     )
            //     .attr('cursor', 'pointer')
            //     .style("stroke", "black")
            //     .style("opacity", .3)
            //     .on("click", function (event, d) {
            //         console.log('event: ', event)

            //         console.log('d: ', d)
            //         let x;
            //         let y;
            //         let zoomLevel;

            //         if (d && d.properties) {
            //             const centroid = path.centroid(d);
            //             x = centroid[0];
            //             y = centroid[1];
            //             zoomLevel = zoomSettings.zoomLevel;
            //         } else {
            //             x = (this.citiesStore.size.width + this.citiesStore.margin.left + this.citiesStore.margin.right) / 2;
            //             y = (this.citiesStore.size.height + this.citiesStore.margin.top + this.citiesStore.margin.bottom) / 2;
            //             zoomLevel = 1;
            //         }
            //     })


                let zoomSettings = {
                    duration: 1000,
                    ease: d3.easeCubicOut,
                    zoomLevel: 4,
                };

                // function clicked(event, d) {

                //     let x;
                //     let y;
                //     let zoomLevel;

                //     if (d && d.properties) {
                //         const centroid = path.centroid(d);
                //         x = centroid[0];
                //         y = centroid[1];
                //         zoomLevel = zoomSettings.zoomLevel;
                //     } else {
                //         x = (this.citiesStore.size.width + this.citiesStore.margin.left + this.citiesStore.margin.right) / 2;
                //         y = (this.citiesStore.size.height + this.citiesStore.margin.top + this.citiesStore.margin.bottom) / 2;
                //         zoomLevel = 1;
                //     }
                // }




            // Create the bubbles
            svg.selectAll('circle')
                .data(markers)
                .enter()
                .append('circle')
                .attr("d", d => d3.geoPath()
                    .projection(projection)
                )
                .attr("cx", d => {
                    // console.log('d.long: ', d.long)
                    // console.log('d.lat: ', d.lat)
                    // console.log('projection: ', projection([d.long, d.lat]))
                        if (projection([d.long, d.lat])) {

                        return projection([d.long, d.lat])[0]
                        }
                        else {
                            console.log('projection([d.long, d.lat]): ', projection([d.long, d.lat]))
                            console.log('d?: ', d)
                        }
                    })
                .attr("cy", d => {
                    if (projection([d.long, d.lat])) {
                        return projection([d.long, d.lat])[1]
                    }
                    })

                .attr('r', d => {
                    // console.log('d.r: ', d)
                    return d.r
                })
                .attr('fill', d => d.color);


var zoom = d3.zoom()
      .scaleExtent([1, 8])
      .on('zoom', function(event) {
          g.selectAll('path')
           .attr('transform', event.transform);
});


            // });
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
    <div id="chartcontainer" class="chart-container outer d-flex" ref="mapContainer">
        <svg id="map-svg" width="100%" height="100%">
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
    border: 1px solid black; /* adds a 1px black border */

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


