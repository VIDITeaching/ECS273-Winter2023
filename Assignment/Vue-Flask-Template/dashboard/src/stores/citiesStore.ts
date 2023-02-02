import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
interface ScatterPoint extends Point{
    cluster: string;
}

export const useCitiesStore = defineStore('cityStore', {
    state: () => ({
        size: { width: 0, height: 0 } as ComponentSize,
        margin: { left: 100, right: 100, top: 100, bottom: 50 } as Margin,
        citiesData: [] 

    }),
    getters: {
        resize: (state) => {
            return state.size
        }
    },
    actions: {
        async fetchCities() { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            axios.get(`${server}/fetchCitiesWithCoords`)
                .then(resp => {
                    // console.log('resp.city: ', resp.data)
                    this.citiesData = resp.data;
                    

                    return true;
                })
                .catch(error => console.log(error));
        },
    }
})