

<script lang="js"> 
import * as d3 from "d3";
import { sankey, sankeyJustify } from "d3-sankey";
import sankeyMixin from "../mixins/sankey-mixin";
import Node from "./Sankey/Node.vue";
import NodeTitle from "./Sankey/NodeTitle.vue";
import Link from "./Sankey/Link.vue";
import Gradient from "./Sankey/Gradient.vue";
import { server } from '../helper';

export default {
  name: "Sankey",
  components: { Node, NodeTitle, Link, Gradient },
  props: {
    data: Object
  },
  mixins: [sankeyMixin],
  data: () => ({
    width: 700,
    height: 600,
    nodes: [],
    links: [],
    sankey: null,
    data: null,
    edgeToRemove: null
  }),
  async mounted() {
    const response = await fetch(
      `${server}/fetchOther`
    );

    let data = await response.json()
    console.log('response',data)
    this.data = data;
  
  },
  methods: {
    removeEdge(edge) {
      console.log(edge);
      // TODO Remove edge functionality
      // const source = edge.source;
      // const target = edge.target;
      // const sourceUsedAnywhere =
      //   this.data.links.filter(
      //     link =>
      //       link.source.name === source.name || link.target.name === source.name
      //   ).length > 1;
      // const targetUsedAnywhere =
      //   this.data.links.filter(
      //     link =>
      //       link.target.name === source.name || link.target.name === target.name
      //   ).length > 1;
      // if (!sourceUsedAnywhere) this.data.nodes.splice(edge.source.index, 1);
      // if (!targetUsedAnywhere) this.data.nodes.splice(edge.target.index, 1);
      // this.data.links.splice(edge.index, 1);
    }
  },
  methods: {
    updateSankey() {
      this.sankey = sankey()
        .nodeAlign(sankeyJustify)
        .nodeWidth(10)
        .nodePadding(10)
        .extent([[0, 0], [this.width, this.height]]);
      const { nodes, links } = this.sankey(this.data);
      this.nodes = nodes;
      this.links = links;
    }
  },
  computed: {
    colors() {
      return d3.interpolateCividis;
    },
    length() {
      return this.nodes.length;
    }
  },
  watch: {
    data: {
      deep: true,
      immediate: true,
      handler(data) {
        // console.log('sankey data: ', data)
        if (!data) return;
        this.updateSankey();
      }
    }
  }
};
</script>


<template>
  <div>
    <svg :width="width" :height="height" v-if="data">
      <g>
        <defs>
          <Gradient
            :colors="colors"
            :data="link"
            :length="length"
            :key="`${link.source.name}-${link.target.name}`"
            v-for="link in links"
          ></Gradient>
        </defs>
        <Link
          :data="link"
          :colors="colors"
          :length="length"
          :key="`${link.source.name}-${link.target.name}`"
          v-for="link in links"
        ></Link>
      </g>
      <g>
        <Node
          :data="node"
          :colors="colors"
          :length="length"
          :width="width"
          :key="node.name"
          v-for="node in nodes"
        ></Node>
        <NodeTitle
          :data="node"
          :colors="colors"
          :length="length"
          :width="width"
          :key="node.name + node.index"
          v-for="node in nodes"
        ></NodeTitle>
      </g>
    </svg>
  </div>
</template>

<!-- <template>
  <h3>hello</h3>
  <div ref="chart"></div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "SankeyDiagram",
  data() {
    return {
      data: {
        nodes: [
          {name: "Node 1", color: "#ff0000"},
          {name: "Node 2", color: "#00ff00"},
          {name: "Node 3", color: "#0000ff"}
        ],
        links: [
          {source: 0, target: 1, value: 10, color: "#ff0000"},
          {source: 1, target: 2, value: 20, color: "#00ff00"}
        ]
      }
    };
  },
  mounted() {
    const width = 800;
    const height = 500;

    const svg = d3
      .select(this.$refs.chart)
      .append("svg")
      .attr("class", "sankey")
      .attr("width", width)
      .attr("height", height);

    const sankey = d3.sankey()
      .nodeWidth(15)
      .nodePadding(10)
      .extent([[1, 1], [width - 1, height - 6]]);

    const {nodes, links} = sankey({
      nodes: this.data.nodes.map(d => Object.assign({}, d)),
      links: this.data.links.map(d => Object.assign({}, d))
    });

    const link = svg
      .append("g")
        .attr("fill", "none")
        .attr("stroke-opacity", 0.5)
      .selectAll("g")
      .data(links)
      .enter().append("g")
        .style("mix-blend-mode", "multiply");

    link.append("path")
        .attr("d", d3.linkHorizontal())
        .attr("stroke", d => d.color)
        .attr("stroke-width", d => Math.max(1, d.width));

    link.append("title")
        .text(d => d.source.name + " → " + d.target.name + "\n" + format(d.value));

    const node = svg
      .append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
      .selectAll("g")
      .data(nodes)
      .enter().append("g");

    node.append("rect")
        .attr("x", d => d.x0)
        .attr("y", d => d.y0)
        .attr("height", d => d.y1 - d.y0)
        .attr("width", d => d.x1 - d.x0)
        .attr("fill", d => d.color)
        .attr("stroke", "#000");

    node.append("text")
        .attr("x", d => d.x0 - 6)
        .attr("y", d => (d.y1 + d.y0) / 2)
        .attr("dy", "0.35em")
        .attr("text-anchor", "end")
        .text(d => d.name);

    node.append("title")
        .text(d => d.name + "\n" + format(d.value));
  }
};
</script> -->