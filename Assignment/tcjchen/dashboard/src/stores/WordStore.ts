import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import { ComponentSize, Margin } from '../types';

export const useStore = defineStore('WordCloudWithInteractionsNew', {
    state: () => ({
        names: [],
        vals: [] as string[],
        size: { width: 0, height: 0 } as ComponentSize,
        margin: { left: 30, right: 20, top: 40, bottom: 40 } as Margin,
        people: ["Moderator", "Trump", "Biden"] as string[],
        selectedPerson: 'Moderator', // default value
    }),
    getters: {
        resize: (state) => {
            return (!isEmpty(state.names) && state.size)
        }
    },
    actions: {
        async fetch(person: string) { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            axios.post(`${server}/fetchWordCloud`, { person: person })
                .then(resp => {
                    this.names = resp.data.data;
                    this.vals = resp.data.freq;
                    return true;
                })
                .catch(error => console.log(error));
        },
    }
})