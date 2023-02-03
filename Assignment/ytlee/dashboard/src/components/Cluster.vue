<script setup lang=ts>
import * as vue from "vue"
import { Ref, ref } from "vue"
import * as d3 from 'd3'
import { BeadClusters, BeadClustersConfig } from './charts/BeadClusters'

const props = defineProps({
    time_slice: Object as () => { year: Number, month: Number },
    data: Object as () => { groups: Any[] },
    metadata: Object as () => Any,
})
const emit = defineEmits(["node-selected"])
const beadClustersChart = new BeadClusters({
        width: 1000,
        height: 800,  
        padding: 10, 
        maxRadius: 3, 
        labelRadius: 10, 
        velocityDecay: 0.4,
})
const nodeSizeScale = vue.computed(() => 
    d3.scaleLog()
        .domain([+props.metadata.min_casualty+2, +props.metadata.max_casualty])
        .range([3, 10])
        .clamp(true)
)

vue.watch(() => props.data.groups, () => {
    draw()
})

vue.onMounted(() => {
    draw()
})

function draw() {
    beadClustersChart.chart(d3.select('#chart'), props.data, nodeSizeScale.value, emit)
}
</script>
<template>
    <div id='chart'>
    </div>
</template>