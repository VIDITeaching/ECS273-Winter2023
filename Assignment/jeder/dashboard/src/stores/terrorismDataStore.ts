import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
interface TerrorismData {
    attacktype1: number, 
    attacktype1_txt: string,
    city: string,
    country: number,
    country_txt: string,
    eventid: number,
    gname: string,
    iday: number,
    imonth: number,
    iyear: number,
    latitude: number,
    longitude: number,
    nkill: number,
    nwound: number,
    region: number,
    region_txt: string,
    success: number,
    suicide: number,
    summary: string,
    targtype1: number,
    targtype1_txt: string,
    weaptype1: number,
    weaptype1_txt: string,
}

export const useTerrorismDataStore = defineStore('terrorismData', {
    state: () => ({
        fromDate: new Date(2001, 8, 1),
        toDate: new Date(2001, 8, 30),
        terrorismData: [] as TerrorismData[],
        terrorismDataFiltered: [] as TerrorismData[],
        selectedIncident: null as null | TerrorismData,
        countrieFilter: null as null | string,
    }),
    actions: {
        async fetchTerrorismData() { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            axios.post(`${server}/fetchTerrorismData`, {  fromDate: this.fromDate, toDate: this.toDate  })
                .then(resp => {
                    this.terrorismData = resp.data;
                    this.filterData();
                    return true;
                })
                .catch(error => console.log(error));
        },
        filterData() {
            const countryNameMap = new Map();
            countryNameMap.set("United States", "United States of America");
            countryNameMap.set("West Bank and Gaza Strip", "Palestine");
            countryNameMap.set("Democratic Republic of the Congo", "Dem. Rep. Congo");
            countryNameMap.set("Serbia-Montenegro", "Montenegro");
            countryNameMap.set("Serbia-Montenegro", "Serbia");

            countryNameMap.set("Republic of the Congo", "Congo");
            countryNameMap.set("Solomon Islands", "Solomon Is.");
            countryNameMap.set("International", "");
            countryNameMap.set("Ivory Coast", "Côte d'Ivoire");
            countryNameMap.set("East Timor", "Timor-Leste");
            countryNameMap.set("Bosnia-Herzegovina", "Bosnia and Herz.");



            this.terrorismDataFiltered = this.terrorismData.filter(d => {
                if (this.countrieFilter != null) {
                    const mapedVal = countryNameMap.has(d.country_txt) ? countryNameMap.get(d.country_txt) : d.country_txt;
                    // console.log(this.countrieFilter + " ?= " + d.country_txt + " -> " + mapedVal);
                    if (this.countrieFilter != mapedVal)
                        return false;
                }
                return true;
            });
            console.log("Filterd to: " + this.countrieFilter + " " + this.terrorismDataFiltered.length);
        }
    }
})