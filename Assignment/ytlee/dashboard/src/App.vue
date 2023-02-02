<script setup lang="ts">
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiInformationOutline } from '@mdi/js'
import Cluster from './components/Cluster.vue';
import TimeAxes from './components/TimeAxes.vue';
import { Ref, ref } from "vue"
import * as vue from 'vue'
import { server } from './helper'

const min_year = 1970
const min_month = 1
const max_year = 2010
const max_month = 12
const time_slice_year: Ref<Number> = ref(2000)
const time_slice_month: Ref<Number> = ref(1)
const time_slice = vue.computed(() => { return { year: time_slice_year.value, month: time_slice_month.value}})
const selected_node: Ref<Any | undefined> = ref(undefined)
const path = mdiInformationOutline

// data
const raw_data: Ref<Any[]> = ref([])
// const data: Ref<any> = ref({groups: []})
const metadata: Ref<any> = ref()
const filtered_data = vue.computed(() => slice_data(raw_data.value, time_slice.value.year, time_slice.value.month))
const data = vue.computed(() => reformat_data(filtered_data.value))
const stackedData = vue.computed(() => reformat_stackedData(raw_data.value))
// const maxAttacks: Ref<Number> = ref(1000)
const maxAttacks = vue.computed(() => Math.max(...stackedData.value.map(year_attacks => Object.keys(year_attacks).filter(key => key != "year").map(country => year_attacks[country]).reduce((partialSum, a) => partialSum + a, 0))))
// const stackedData: Ref<any> = ref()
// vue.watch(time_slice, () => {
//     console.log("slicing data")
//     filtered_data = slice_data(raw_data.value, time_slice.value.year, time_slice.value.month)
//     data.value.groups = reformat_data(filtered_data)
//     stackedData.value = reformat_stackedData(filtered_data)
// })

async function fetch_data() {
    console.log(server)
    await fetch(`${server}/fetchData`)
        .then(res => res.json())
        .then(json => {
            console.log("data fetched", json)
            raw_data.value = json.data
            metadata.value = json.metadata
            console.log(metadata.value)
            // const filtered_data = slice_data(raw_data.value, time_slice.value.year, time_slice.value.month)
            // data.value.groups = reformat_data(filtered_data)
            // stackedData.value = reformat_stackedData(filtered_data)
        }
    )
}

function slice_data(raw_data, year, month) {
    const filtered_data = {}
    Object.keys(raw_data).forEach(country => {
        filtered_data[country] = raw_data[country].filter(attack => 
            // +attack.date.split("-")[0] == year && +attack.date.split("-")[1] == month
            +attack.date.split("-")[0] == year && attack.attack_type == "Bombing/Explosion"
        )
    })
    console.log(filtered_data, year, month)
    return filtered_data
}


function reformat_stackedData(raw_data) {
  let attacks_groupby_year = {}
  Object.keys(raw_data).forEach(country => {
    raw_data[country].forEach(attack => {
      const year = +attack.date.split("-")[0]
      if(attacks_groupby_year[year] == undefined) attacks_groupby_year[year] = {}
      if(attacks_groupby_year[year][country] == undefined) attacks_groupby_year[year][country] = 0
      attacks_groupby_year[year][country] += 1
    })
  })

  // convert to array indexed by year 
  let res = []
  for(let year = min_year; year < max_year+1; year++) {
    if(attacks_groupby_year[year] == undefined) {
      let empty_year = { year: year }
      Object.keys(raw_data).forEach(country => {
        empty_year[country] = 0
      })
      res.push(empty_year)
      continue
    }

    attacks_groupby_year[year].year = year
    Object.keys(raw_data).forEach(country => {
      if(attacks_groupby_year[year][country] == undefined) attacks_groupby_year[year][country] = 0
    })
    res.push(attacks_groupby_year[year])
  }

  return res
}

function reformat_data(filtered_data) {
    const total_attacks = Object.keys(filtered_data).map(country => filtered_data[country].length).reduce((partialSum, a) => partialSum + a, 0)
    console.log(total_attacks)
    let res = []
    Object.keys(filtered_data).forEach(country => {
        const percentage = filtered_data[country].length / total_attacks
        res.push({
            'label': country,
            'percentage': percentage,
            'key': country,
            'numNodes': filtered_data[country].length,
            'nodeData': filtered_data[country].map(attack => attack.casualty),
            'summary': filtered_data[country].map(attack => attack.summary),
            'kill': filtered_data[country].map(attack => attack.kill),
            'wound': filtered_data[country].map(attack => attack.wound),
            'attack_type': filtered_data[country].map(attack => attack.attack_type),
            'target': filtered_data[country].map(attack => attack.target),
            'motive': filtered_data[country].map(attack => attack.motive),
            'notes': filtered_data[country].map(attack => attack.notes),
        })
    })
    return { groups: res }
}

vue.onBeforeMount(() => {
    fetch_data()
})

function highlight_digits(summary) {
  const isdigit = /^\d+$/
  const words = summary.split(" ")
  let res = ""
  words.forEach(word => {
    const stripped_word = word.replace(/[.,#!$%\^&\*;:{}=\-_`~()]/g, "")
    if(isdigit.test(stripped_word) || isDigitSemantic(stripped_word)) res += wrap_highlight(word)
    else res += word
    res += " "
  })
  return res
}

function isDigitSemantic(text) {
  const units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]
  const tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
  const scales = ["hundred", "thousand", "million", "billion", "trillion"]
  return units.includes(text) || tens.includes(text) || scales.includes(text)
}

function wrap_highlight(content) {
  console.log("add highlight: ", content)
    const highlight_color = "#ee1f1fc9"
    return `<span style='background-color:${highlight_color};'>${content}</span>`
}

function get_top_n(dict, n=3) {
  const list = Object.keys(dict).map(key => { return {key: key, value: dict[key]}})
  const res = list.sort((a, b) => a.value < b.value).slice(0, n)
  console.log(res)
  return res

}
</script>

<template>
  <v-app>
    <div id="main-container" class="d-flex flex-row flex-nowrap" fluid>
      <div class="left-section d-flex flex-column justify-center align-center">
        <h2 class="component-header cluster-header">
          Exploration of Bombing/Explosion attacks
          <div class=tooltip> 
            <svg-icon class="info-icon" type="mdi" :path="path">
            </svg-icon>
            <span class="tooltiptext top-tooltiptext" style="width: 500px">
              This force-directed cluster encodes data on Bombing/Explosion events annually.
              <br>
              Each node represents an attack, clustered by attacked region.
              <br>
              Node size encodes casualty (kill + wound).
              <br>
              Click any node to inspect more detail on the event.
              <br>
              <br>
              The stacked area chart encodes total events of each region in a year.
              <br>
              Use the slider to explore bombing attacks by year.
              <br>
            </span>
          </div>
        </h2>
        <Cluster class='cluster-container' 
          v-if="metadata"
          :data="data"
          :metadata="metadata"
          :time_slice="time_slice"
          @node-selected="(d) => selected_node=d"/>
        <div class="slider-container d-flex flex-row justify-center align-center">
          <TimeAxes class=timeaxes-container 
            v-if="metadata"
            :data="stackedData"
            :yMax="maxAttacks"
            :target_year="time_slice_year"
            :dateRange="[min_year, max_year]"/>
          <v-slider v-model="time_slice_year"
            v-if="metadata"
            :max="max_year"
            :min="min_year"
            :step="1"
            thumb-label
          ></v-slider>
        </div>
      </div>
      <div v-if="selected_node" class=right-section>
        <div class=summary-container>
          <h2 class="component-header summary-header"> {{selected_node.isClusterNode? "Cluster ": ""}}Summary </h2>
          <div v-if="selected_node.isClusterNode" class=summary-content> Cluster: {{ selected_node.key }}</div>
          <div v-if="selected_node.isClusterNode" class=summary-content> Total events: {{ selected_node.summary }}</div>
          <div v-else class=summary-content v-html="highlight_digits(selected_node.summary)">  </div>
        </div>
        <div class=casualty-container>
          <h2 class="component-header casualty-header"> Reported Casualty {{selected_node.isClusterNode? "(Annual)": "" }} </h2>
          <div class=kill-content> Kill: {{ selected_node.kill }} </div>
          <div class=wound-content> Wound: {{ selected_node.wound }} </div>
        </div>
        <div class=info-container>
          <h2 class="component-header info-header"> Other Information </h2>
          <!-- <div v-if="selected_node.isClusterNode" class=attack-type-content> 
            &nbsp;
            <span class="content-header"> Top 3 Attack Types: </span>
            <div v-for="attack_type in get_top_n(selected_node.attack_type, 3)"> 
              &nbsp; &#x2022; {{ attack_type.key }} : {{ attack_type.value }}
            </div>
          </div>
          <div v-else class=attack-type-content> 
            <span class="content-header"> Attack Types:  </span>
            {{ selected_node.attack_type }}
          </div> -->
          <div v-if="selected_node.isClusterNode" class=target-type-content> 
            &nbsp;
            <span class="content-header"> Top 3 Targets: </span>
            <div v-for="target in get_top_n(selected_node.target, 3)"> 
              &nbsp; &#x2022; {{ target.key }} : {{ target.value }}
            </div>
          </div>
          <div v-else class=target-type-content> 
            <span class=content-header> Targets: </span>
            {{ selected_node.target}}
          </div>
          <div v-if="!selected_node.isClusterNode" class=motive-content> 
            <span class=content-header> Motive: </span>
            {{ selected_node.motive }} 
          </div>
          <div v-if="!selected_node.isClusterNode" class=notes-container>
            <h2 class="component-header notes-header"> Additional Notes </h2>
            <div class=notes-content> {{ selected_node.notes }} </div>
          </div>
        </div>

      </div>
    </div>
  </v-app>
</template>

<style scoped>
#main-container{
  height: 95%;
  margin: 1%;
}

.left-section {
  width: 70%;
  height: 100%;
}
.right-section {
  width: 30%;
  height: 100%;
}
.component-header {
  margin: 1% 1% 1% 0%;
  border-bottom: solid 1px #b7b7b7;
  font-family: 'Lato';
  font-weight: bold;
  background: #f7f7f7;
  width: 100%;
  padding-left: 1%;
}
.slider-container {
  width: 80%;
  height: 100%;
  align-items: center;
  justify-content: center;
  position: relative;
  margin-left: 1px;
}
.cluster-container {
  width: 100%;
  height: 90%;
}
.timeaxes-container {
  position: absolute;
  width: 100%;
  top: 50%;
  left: 0;
}
:deep(.v-input__details) {
  position: absolute !important;
}
:deep(.v-slider-track__fill) {
  width: 0px !important;
}
.v-slider.v-input--horizontal {
  align-items: center;
  margin-inline-start: unset !important;
  margin-inline-end: unset !important;
}
.info-icon {
  position: absolute;
  top: 3%;
  left: 67%;
}
.tooltip {
  cursor: pointer;
}
.tooltip .tooltiptext {
  visibility: hidden;
  background-color: white;
  /* text-align: center; */
  padding: 5px 5px;
  border-radius: 6px;
  border: solid 1px black;
  /* Position the tooltip text */
  position: absolute;
  z-index: 3;
  /* Fade in tooltip */
  opacity: 0;
  transition: opacity 0.3s;
  font-family: Georgia;
  font-weight: normal;
  font-size: 1rem;
}

.tooltip .top-tooltiptext {
  /* width: 120px; */
  margin-left: -60px;
  /* bottom: 100%; */
  left: 50%;
  margin-top: 20px;
}

.tooltip .right-tooltiptext {
  left: 39%;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>
