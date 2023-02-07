import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
interface ScatterPoint extends Point{
    cluster: string;
}

export const useHousingStore = defineStore('housingInteractions', {
    state: () => ({

        points: [] as ScatterPoint[],
        clusters: [] as string[],
        housing: '' as string,
        size: { width: 0, height: 0 } as ComponentSize,
        margin: { left: 75, right: 50, top: 100, bottom: 50 } as Margin,
        methods: ['PCA', 't-SNE'] as string[],
        selectedMethod: 'PCA', // default value
    }),
    getters: {
        resize: (state) => {
            return (state.size)
        }
    },
    actions: {
        async fetchHousing(method: string) { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            axios.post(`${server}/fetchHousing`, {method: method})
                .then(resp => {
                    this.housing = resp.data;
                    return true;
                })
                .catch(error => console.log(error));
        },
    }
})