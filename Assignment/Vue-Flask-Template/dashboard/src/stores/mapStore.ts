import { defineStore } from 'pinia'
import axios from "axios"
import { server } from '../helper';

export const useMapStore = defineStore('mapStore', {
    state: () => ({
        map: {}

    }),
    actions: {
        async fetchMap() { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            axios.get(`${server}/fetchMap`)
                .then(resp => {
                    // console.log('resp.city: ', resp.data)
                    this.map = resp.data;
                    return true;
                })
                .catch(error => console.log(error));
        },
    }
})