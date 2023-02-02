
<script lang="ts">
import * as d3 from "d3";

import { useTerrorismDataStore } from '../stores/terrorismDataStore';
import Datepicker from 'vue3-datepicker'


const margin = { top: 40, right: 10, bottom: 20, left: 10 };
const width = 700;
const height = 400;


export default {
    components: {
        Datepicker
    },

    data() {
        return {
            fromDate: new Date(2001, 8, 1),
            toDate: new Date(2001, 8, 30),
        }
    },
    setup() { // Composition API syntax
        const store = useTerrorismDataStore()
        return {
            store, // Return store as the local state, but when you update the property value, the store is also updated.
        }
    },
    created() {
    },
    methods: {
        initChart() {

            // console.log("Init Chart")


        },
    },
    watch: { // updated because a legend is added.
        fromDate(newValue) {
            // console.log('newValue', newValue);
            this.store.fromDate = this.fromDate;
            this.store.fetchTerrorismData();
        },
        toDate(newValue) {
            // console.log('newValue', newValue);
            this.store.toDate = this.toDate;
            this.store.fetchTerrorismData();
        },

    },
    mounted() {
    },
    beforeDestroy() {
    }
}

</script>

<template>
    <h3 class="ma-2">Filter</h3>
    <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
        <v-row justify="center" no-gutters>
            <v-col>
                <p style="display:inline">From:</p>
                <Datepicker class="datepicker" v-model="this.fromDate" startingView='year' />
            </v-col>
            <v-col>

                <p style="display:inline">To:</p>
                <Datepicker class="datepicker" v-model="this.toDate" startingView='year' />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <p> Loading can take ~1min after changing the date (processing ~150k attacks)</p>
            </v-col>
        </v-row>
    </v-container>

    <!-- <v-btn @click="" elevation="2">
        Have clicked this times
    </v-btn> -->

</template>


<style>
.datepicker {
    border-style: solid;
    border-color: grey;
    border-radius: 10;
}
</style>