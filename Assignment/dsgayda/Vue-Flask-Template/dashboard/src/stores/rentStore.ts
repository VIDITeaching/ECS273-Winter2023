import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
interface ScatterPoint extends Point{
    cluster: string;
}

export const useRentStore = defineStore('rentInteractions', {
    state: () => ({

        points: [] as ScatterPoint[],
        clusters: [] as string[],
        rent: [],
        size: { width: 0, height: 0 } as ComponentSize,
        margin: { left: 20, right: 20, top: 20, bottom: 40 } as Margin,
        methods: ['PCA', 't-SNE'] as string[],
        selectedMethod: 'PCA', // default value
    }),
    getters: {
        resize: (state) => {
            return (state.size)
        }
    },
    actions: {
        async fetchRent(method: string) { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            axios.post(`${server}/fetchRent`, {method: method})
                .then(resp => {
                    this.rent = resp.data;
                    return true;
                })
                .catch(error => console.log(error));
        },
    }
})