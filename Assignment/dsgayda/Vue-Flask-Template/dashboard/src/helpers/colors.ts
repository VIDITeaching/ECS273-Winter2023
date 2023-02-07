import * as d3 from 'd3';

export const getColors = (keys: string[]) => {
    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
    const colors = colorScale
    .domain(keys.sort((a, b) => a.localeCompare(b)))
    .range(d3.schemeTableau10);

    return colors;
}
