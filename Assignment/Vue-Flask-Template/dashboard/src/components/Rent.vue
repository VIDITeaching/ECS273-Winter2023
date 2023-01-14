<script lang="ts">
import * as d3 from "d3";
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
// A "extends" B means A inherits the properties and methods from B.
interface ScatterPoint extends Point{ 
    cluster: string;
}

// Computed property: https://vuejs.org/guide/essentials/computed.html
// Lifecycle in vue.js: https://vuejs.org/guide/essentials/lifecycle.html#lifecycle-diagram

export default {
    data() {
        console.log('dataatata')
        // d3.csv('rent_subset.csv').then((data) => {
        //     console.log('data:', data)
        // })
        // Here we define the local states of this component. If you think the component as a class, then these are like its private variables.
        return {
            // points: [] as ScatterPoint[], // "as <Type>" is a TypeScript expression to indicate what data structures this variable is supposed to store.
            // clusters: [] as string[],
            // size: { width: 0, height: 0 } as ComponentSize,
            // margin: {left: 20, right: 20, top: 20, bottom: 40} as Margin,
        }
    },
    computed: {
        // Re-render the chart whenever the window is resized or the data changes (and data is non-empty)
        rerender() {
            
        }
    },
    created() {
        // fetch the data via API request when we init this component. This will only get called once.
        // In axios anything we send back in the response are always bound to the "data" property.
        axios.get(`${server}/fetchRent`)
            .then(resp => { // check out the app.py in ./server/ to see the format
                // this.points = resp.data; 
                console.log('hey!')
                console.log('resp.data:', resp.data)
                // this.clusters = resp.data.clusters;
                return true;
            })
            .catch(error => console.log(error));
        // console.log('data:')
        // d3.csv('rent_subset.csv').then((data) => {
        //     console.log('data:', data)
        // })

    },
    methods: {
    
    },
    watch: {
       
    },
    // The following are general setup for resize events.
    mounted() {
    },
    beforeDestroy() {
   
    }
}
</script>

<!-- "ref" registers a reference to the HTML element so that we can access it via the reference in Vue.  -->
<!-- We use flex to arrange the layout-->
<template>
    <h3>hello!</h3>
    <div class="chart-container d-flex" ref="scatterContainer">
        <svg id="scatter-svg" width="100%" height="100%">
            <!-- all the visual elements we create in initChart() will be inserted here in DOM-->
        </svg>
    </div>
</template>

<style scoped>
.chart-container{
    height: 100%;
}
</style>