import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
interface ScatterPoint extends Point{
    cluster: string;
}
interface DryBean {
    Area: number;
    // Perimeter: number;
    // MajorAxisLength: number;
    // MinorAxisLength: number;
    AspectRation: number;
    // Eccentricity: number;
    ConvexArea: number;
    // EquivDiameter: number;
    // Extent: number;
    // Solidity: number;
    // roundness: number;
    Compactness: number;
    // ShapeFactor1: number;
    // ShapeFactor2: number;
    // ShapeFactor3: number;
    // ShapeFactor4: number;
    Class: string;
}

export const useExampleStore = defineStore('exampleWithInteractions', {
    state: () => ({
        points: [] as ScatterPoint[],
        bean_data: [] as DryBean[],
        clusters: [] as string[],
        columns: [] as string[],
        attributes: [] as string[],
        selectedMethod: [] as string[],
        size: { width: 0, height: 0 } as ComponentSize,
        margin: { left: 20, right: 20, top: 20, bottom: 40 } as Margin,
        methods: ['PCA', 't-SNE', 'UMAP', 'scatter'] as string[],
        selectedMethod: 'scatter', // default value
        // =====================================================
        padding: 25,
    }),
    getters: {
        resize: (state) => {
            return (!isEmpty(state.points) && state.size)
        }
    },
    actions: {
        async fetchExample(method: string) { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            axios.post(`${server}/fetchExample`, {method: method})
                .then(resp => {
                    // console.log(resp.data.data);
                    console.log('method ======')
                    console.log(method)
                    this.select_method = method;

                    if(this.select_method == 'scatter'){
                        this.bean_data = resp.data.data;
                        console.log('method - scatter')
                    }
                    else { // PCA, t-SNE, UMAP
                        this.points = resp.data.data;
                    }
                    this.clusters = resp.data.clusters;
                    this.columns = resp.data.columns;
                    console.log(this.columns);

                    return true;
                })
                .catch(error => console.log(error));
        },
    }
})