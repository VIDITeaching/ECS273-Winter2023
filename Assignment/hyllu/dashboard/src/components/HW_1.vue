<script lang="ts">
import * as d3 from "d3";
import { sankey as d3Sankey, sankeyLinkHorizontal as d3SsankeyLinkHorizontal } from 'd3-sankey';
import axios from 'axios';
import { isEmpty, debounce, takeWhile } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
interface ScatterPoint extends Point{
    cluster: string;
}

/* The new major things from Example.vue
1) initLegend() in this component
2) the template and the css in this component
*/

export default {
    data() {
        return {
            points: [] as ScatterPoint[],
            clusters: [] as string[],
            size: { width: 0, height: 0 } as ComponentSize,
            margin: {left: 20, right: 20, top: 20, bottom: 40} as Margin,
            coors: [] as string[],
            nodes: [],
            links: [],
            link_set: [],
            selected_ids: [],
            selected_sets: [],
            network_nodes: [],
            network_links: [],
            network_positions: [],
            network_notes: "",
            network_data: false,
        }
    },
    computed: {
        rerender() {
            // return (!isEmpty(this.points))  && this.size
            return (!isEmpty(this.coors))  && this.size
        },
        rerender_network() {
            return (!isEmpty(this.network_positions)) && this.size
        }
    },
    created() {
        // axios.get(`${server}/fetchExample`)
        //     .then(resp => {
        //         this.points = resp.data.data;
        //         this.clusters = resp.data.clusters;
        //         return true;
        //     })
        //     .catch(error => console.log(error));
        
        axios.get(`${server}/fetchTwitch`)
            .then(resp => {
                this.coors = resp.data.coors;
                this.nodes = resp.data.nodes;
                this.links = resp.data.links;
                this.link_set = resp.data.link_set;
                this.selected_ids = [];
                this.selected_sets = [];
                console.log(resp.data);
                return true;
            })
            .catch(error => console.log(error));
    },
    methods: {
        onResize() {
            let target = this.$refs.parallelsetContainer as HTMLElement
            if (target === undefined || target === null) return;
            this.size = { width: target.clientWidth, height: target.clientHeight };
        },
        initChart_parallelset() {
            const chartThis = this;

            let chartContainer = d3.select('#parallelset-svg')
            console.log(this.coors);
            console.log(this.nodes);

            // init sankey
            let sankey = d3Sankey()
                .nodeSort(null)
                .linkSort(null)
                .nodeWidth(4)
                .nodePadding(20)
                .extent([[0, 5], [this.size.width, this.size.height - 5]])

            // draw chart svg
            const {nodes, links} = sankey({
                nodes: this.nodes.map(d => Object.assign({}, d)),
                links: this.links.map(d => Object.assign({}, d))
            });

            // let color = d3.scaleOrdinal(["NO"], ["#da4f81"]).unknown("#ccc") // .attr("stroke", d => color(d.names[0]))

            chartContainer.append("g")
                .selectAll("rect")
                .data(nodes)
                .join("rect")
                .attr("x", d => d.x0)
                .attr("y", d => d.y0)
                .attr("height", d => d.y1 - d.y0)
                .attr("width", d => d.x1 - d.x0)
                .append("title")
                .text(d => `${d.name}\n${d.value.toLocaleString()}`);

            chartContainer.append("g")
                .attr("fill", "none")
                .selectAll("g")
                .data(links)
                .join("path")
                .attr("d", d3SsankeyLinkHorizontal())
                .attr("stroke", "#ccc")
                .attr("stroke-width", d => d.width)
                .attr("index", (d, i) => i)
                .on("click", select_bar)
                .style("mix-blend-mode", "multiply")
                .append("title")
                .text(d => `${d.names.join(" → ")}\n${d.value.toLocaleString()}`);

            function select_bar() {
                if (this.getAttribute('stroke') == "#ccc" || this.getAttribute('stroke') == "rgb(204, 204, 204)") {
                    d3.select(this).transition()
                        .duration('50')
                        .attr('stroke', "#99c");
                    chartThis.selected_sets.push(this.getAttribute('index'));
                }
                else {
                    d3.select(this).transition()
                        .duration('50')
                        .attr('stroke', "#ccc");
                    let tmp_id = chartThis.selected_sets.indexOf(this.getAttribute('index'));
                    chartThis.selected_sets.splice(tmp_id, 1);
                }
                console.log(chartThis.selected_sets);
                chartThis.initChart_network();
            };

            chartContainer.append("g")
                .style("font", "10px sans-serif")
                .selectAll("text")
                .data(nodes)
                .join("text")
                .attr("x", d => d.x0 < this.size.width / 2 ? d.x1 + 6 : d.x0 - 6)
                .attr("y", d => (d.y1 + d.y0) / 2)
                .attr("dy", "0.35em")
                .attr("text-anchor", d => d.x0 < this.size.width / 2 ? "start" : "end")
                .text(d => d.name)
                .append("tspan")
                .attr("fill-opacity", 0.7)
                .text(d => ` ${d.value.toLocaleString()}`);
        },
        initChart_network() {
            const chartThis = this;
            this.selected_ids = [];
            this.selected_sets.forEach(element => {
                this.selected_ids.push(this.link_set[element]);
            });
            console.log(this.selected_ids);

            axios.post(`${server}/fetchTwitch`, {set:this.selected_sets, id:this.selected_ids})
                .then(resp => {
                    this.network_notes = resp.data.notes;
                    this.network_nodes = resp.data.nodes;
                    this.network_links = resp.data.links;
                    this.network_positions = resp.data.positions;
                    // console.log(resp.data);
                    this.network_data = true;
                    this.drawChart_network();
                    return true;
                })
                .catch(error => console.log(error));
            // while (!this.network_data) {
            // }
            // console.log("data is here");
        },
        drawChart_network() {
            console.log(this.network_notes);
        },
        initLegend() {
            let legendContainer = d3.select('#scatter-legend-svg')

            let clusterLabels: string[] = this.clusters.map((cluster: string, idx: number) => `Cultivar ${idx+1}`)
            let colorScale = d3.scaleOrdinal().domain(clusterLabels).range(d3.schemeTableau10)

        }
    },
    watch: { // updated because a legend is added.
        rerender(newSize) {
            if (!isEmpty(newSize)) {
                // d3.select('#scatter-svg').selectAll('*').remove()
                d3.select('#parallelset-svg').selectAll('*').remove()
                // d3.select('#scatter-legend-svg').selectAll('*').remove()
                this.initChart_parallelset()
                // this.initChart_network()
                this.initLegend()
            }
        },
        rerender_network(newSize) {
            if (!isEmpty(newSize)) {
                // d3.select('#scatter-svg').selectAll('*').remove()
                d3.select('#network-svg').selectAll('*').remove()
                // d3.select('#scatter-legend-svg').selectAll('*').remove()
                // this.initChart_parallelset()
                this.drawChart_network()
                // this.initLegend()
            }
        },
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
    <div class="viz-container justify-end">
        <div class="chart-container" ref="parallelsetContainer">
            <!-- <svg id="scatter-svg" width="100%" height="100%">
            </svg> -->
            <svg id="parallelset-svg" width="100%" height="100%"></svg>
        </div>
        <div class="chart-container d-flex" ref="networkContainer">
            <svg id="network-svg" width="80%" height="100%"></svg>
            <svg id="scatter-legend-svg" width="20%" height="100%"></svg>
        </div>
        <!-- <div id="scatter-legend-container" class="d-flex">
            <svg id="scatter-legend-svg" width="100%" height="100%">
            </svg>
        </div> -->
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
    /* width: calc(100% - 5rem); */
    width: 100%;
    height: 50%;
}
/* #scatter-legend-container{
    width: 5rem;
} */
</style>