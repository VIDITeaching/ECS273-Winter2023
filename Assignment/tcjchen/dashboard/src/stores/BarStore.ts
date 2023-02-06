import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import { ComponentSize, Margin } from '../types';

export const useStore = defineStore('BarWithInteractions', {
    state: () => ({
        scores: [],
        emotion: [] as string[],
        people: [] as string[],
        size: { width: 0, height: 0 } as ComponentSize,
        margin: { left: 30, right: 20, top: 40, bottom: 40 } as Margin,
        methods: ["Overall", "Supreme Court", "Covid-19", "Economy", "Race and Violence", "Records", "Integrity"] as string[],
        selectedMethod: 'Overall', // default value
    }),
    getters: {
        resize: (state) => {
            return (!isEmpty(state.scores) && state.size)
        }
    },
    actions: {
        async fetchExample(method: string) { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            axios.post(`${server}/fetchExample`, { method: method })
                .then(resp => {
                    this.scores = resp.data.data;
                    this.emotion = resp.data.emotion;
                    this.people = resp.data.people;
                    return true;
                })
                .catch(error => console.log(error));
        },
    }
})