<script lang='ts'>
import * as d3 from 'd3';
import axios from 'axios';
import { isEmpty, debounce } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
import { cluster } from 'd3';
import { createStructuralDirectiveTransform } from '@vue/compiler-core';
import {legend as Legend} from "@d3/color-legend"
import { anyTypeAnnotation } from '@babel/types';
import { d3_parcoords } from '../../../dashboard/d3.parcoords.js'

interface RentData {
  post_id: string;
  date: number;
  year: number;
  nhood: string;
  city: string;
  county: string;
  price: number;
  beds: number;
  baths: number | null;
  sqft: number | null;
  room_in_apt: number;
  address: number | null;
  lat: number | null;
  lon: number | null;
  title: string;
  descr: number | null;
  details: number | null;
}    

/* The new major things from Example.vue
1) initLegend() in this component
2) the template and the css in this component
*/

export default {
    data() {
        return {
            rentData: [] as RentData[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 40, right: 50, top: 20, bottom: 50} as Margin,
            brushHeight: 50,
            selections: new Map(),
            dselectedColor: '#ddd',
            x: new Map(),
            z: d3.scaleSequential,
            svg: d3.select('#scatter-svg'),

        }
    },
    computed: {
        rerender() {
            return (!isEmpty(this.rentData)) && this.size
        }
    },
    created() {
        console.log('create');
        axios.post(`${server}/fetchTinyRent`)
            .then(resp => {
                this.rentData = resp.data.data;
                this.initChart()
                return true;
            })
            .catch(error => console.log(error));
        
    },
    methods: {
        onResize() {  // record the updated size of the target element
            let target = this.$refs.scatterContainer as HTMLElement
            if (target === undefined) return;
            this.size = { width: target.clientWidth, height: target.clientHeight };
        },
        initChart() {
            var data = [
            [0,-0,0,0,0,3 ],
            [1,-1,1,2,1,6 ],
            [2,-2,4,4,0.5,2],
            [3,-3,9,6,0.33,4],
            [4,-4,16,8,0.25,9]
            ];

            let pc = d3_parcoords()("#example")
            .data(data)
            .render()
            .createAxes();

            let keys = Object.keys(this.rentData[0]);
            this.x = new Map(Array.from(keys, key => [key, d3.scaleLinear(d3.extent(this.rentData, d => d[key]), [this.margin.left, this.size.width - this.margin.right])]));
            let y = d3.scalePoint(keys, [this.margin.top, this.size.height - this.margin.bottom]);
            console.log('keys:', this.y);
            
            let colors = d3.interpolateBrBG;
            let label = d => d.name;
            this.size.height = keys.length * 120;
            this.z = d3.scaleSequential(this.x.get(keys[0]).domain().reverse(), colors);
            let line = d3.line().defined(([, value]) => value != null).x(([key, value]) => this.x.get(key)(value)).y(([key]) => y(key));

            const brush = d3.brushX()
                .extent([
                    [this.margin.left, -(this.brushHeight / 2)],
                    [this.size.width - this.margin.right, this.brushHeight / 2]
                ])
                .on("start brush end", this.brushed);

            const path = this.svg.append("g")
                .attr("fill", "none")
                .attr("stroke-width", 1.5)
                .attr("stroke-opacity", 0.4)
                .selectAll("path")
                .data(this.rentData.slice().sort((a, b) => d3.ascending(a[keys], b[keys])))
                .join("path")
                .attr("stroke", d => this.z(d[keys]))
                .attr("d", d => line(d3.cross(keys, [d], (key, d) => [key, d[key]])));

            path.append("title")
                .text(label);

            this.svg.append("g")
                .selectAll("g")
                .data(keys)
                .join("g")
                .attr("transform", d => `translate(0,${y(d)})`)
                .each(function(d) { d3.select(this).call(d3.axisBottom(this.x.get(d))); })
                .call(g => g.append("text")
                    .attr("x", this.margin.left)
                    .attr("y", -6)
                    .attr("text-anchor", "start")
                    .attr("fill", "currentColor")
                    .text(d => d))
                .call(g => g.selectAll("text")
                    .clone(true).lower()
                    .attr("fill", "none")
                    .attr("stroke-width", 5)
                    .attr("stroke-linejoin", "round")
                    .attr("stroke", "white"))
                .call(brush);


        },
        brushed({ selection }, key) {
            if (selection === null) this.selections.delete(key);
            else this.selections.set(key, selection.map(this.x.get(key).invert));
            const selected = [];
            path.each(function(d) {
            const active = Array.from(this.selections).every(([key, [min, max]]) => d[key] >= min && d[key] <= max);
            d3.select(this).style("stroke", active ? this.z(d[keys]) : this.deselectedColor);
            if (active) {
                d3.select(this).raise();
                selected.push(d);
            }
            });
            this.svg.property("value", selected).dispatch("input");
        }
    },
    watch: {
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                d3.select('#scatter-svg').selectAll('*').remove()
                d3.select('#scatter-legend-svg').selectAll('*').remove()
                this.initChart()
            }
        }
    },
    mounted() {
        window.addEventListener('resize', debounce(this.onResize, 100)) 
        this.onResize()
    },
    beforeDestroy() {
       window.removeEventListener('resize', this.onResize)
    }
}
</script>

<!-- We use flex to arrange the layout-->
<template>
    <div class='viz-container d-flex justify-end'>
        <div class='chart-container d-flex' ref='scatterContainer'>
            <svg id='scatter-svg' width='100%' height='100%'>
            </svg>
        </div>
        <div id="example" class="parcoords" style="width:360px;height:150px"></div>
        <div id='scatter-legend-container' class='d-flex'>
            <svg id='scatter-legend-svg' width='100%' height='100%'>
            </svg>
        </div>
    </div>
</template>

<!-- How we arrange the two svgs with css-->
<style scoped>
.viz-container{
    height:100%;
    flex-direction: row;
    flex-wrap: nowrap;
}
.chart-container{
    width: calc(100% - 5rem);
    height: 100%;
}
#scatter-legend-container{
    width: 6rem;
    flex-shrink: 0;
    overflow: auto;
}
.parcoords > canvas {
  font: 14px sans-serif;
  position: absolute;
}
.parcoords > canvas {
  pointer-events: none;
}
.parcoords text.label {
  cursor: default;
}
.parcoords rect.background:hover {
  fill: rgba(120,120,120,0.2);
}
.parcoords canvas {
  opacity: 1;
  transition: opacity 0.3s;
  -moz-transition: opacity 0.3s;
  -webkit-transition: opacity 0.3s;
  -o-transition: opacity 0.3s;
}
.parcoords canvas.faded {
  opacity: 0.25;
}
.parcoords {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  background-color: white;
}
</style>