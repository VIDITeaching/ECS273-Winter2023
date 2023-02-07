import * as d3 from 'd3';

let startYear = 1990;
let endYear = 2018;
let currentYear = 2000;

let startStackedYear = 1990;
let endStackedYear = 2018;
let currentStackedYear = 1990;

export const setStartYear = (year: number) => {
    startYear = year;
    setCurrentYear(year);
    // console.log('set startYear: ', startYear)
}


export const setEndYear = (year: number) => {
    endYear = year;
    // console.log('set endYear: ', endYear)
}


export const setCurrentYear = (year: number) => {
    currentYear = year;
    // console.log('set currentYear: ', currentYear)
}

export const getStartYear = () => {
    return startYear;
}


export const getEndYear = () => {
    return endYear;
}


export const getCurrentYear = () => {
    return currentYear;
}


export const setStackedStartYear = (year: number) => {
    startStackedYear = year;
    // setStackedCurrentYear(year);
    // console.log('set startYear: ', startYear)
}


export const setStackedEndYear = (year: number) => {
    endStackedYear = year;
    // console.log('set endYear: ', endYear)
}


export const setStackedCurrentYear = (year: number) => {
    currentStackedYear = year;
    // console.log('set currentYear: ', currentYear)
}

export const getStackedStartYear = () => {
    return startStackedYear;
}


export const getStackedEndYear = () => {
    return endStackedYear;
}


export const getStackedCurrentYear = () => {
    return currentStackedYear;
}