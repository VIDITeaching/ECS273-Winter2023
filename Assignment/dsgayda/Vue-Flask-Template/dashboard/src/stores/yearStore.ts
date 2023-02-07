// store.js
import { defineStore } from 'pinia';

export const useYearStore = defineStore('yearStore', {
    state: () => ({
        year: 1990

    }),
    actions: {
        getYear() { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            return this.year;
        },
        async setYear(newYear) { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            this.year = newYear;
        },
    }
})