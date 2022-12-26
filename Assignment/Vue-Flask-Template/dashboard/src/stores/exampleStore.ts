import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
interface ScatterPoint extends Point{
    cluster: string;
}

export const useExampleStore = defineStore('exampleWithInteractions', {
    state: () => ({
        points: [] as ScatterPoint[],
        clusters: [] as string[],
        size: { width: 0, height: 0 } as ComponentSize,
        margin: { left: 20, right: 20, top: 20, bottom: 40 } as Margin,
        methods: ['PCA', 't-SNE'] as string[],
        selectedMethod: 'PCA',
    }),
    getters: {
        resize: (state) => {
            return (!isEmpty(state.points) && state.size)
        }
    },
    actions: {
        async fetchExample(method: string) {
            axios.post(`${server}/fetchExample`, {method: method})
                .then(resp => {
                    this.points = resp.data.data;
                    this.clusters = resp.data.clusters;
                    return true;
                })
                .catch(error => console.log(error));
        },
    }
})