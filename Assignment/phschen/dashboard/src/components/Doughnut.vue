<template>
    <!-- <h1>Doughnut Chart</h1> -->
    <h2>Total production of housing in each county</h2>
    <Doughnut
      :chart-options="chartOptions"
      :chart-data="chartData"
      :chart-id="chartId"
      :dataset-id-key="datasetIdKey"
      :plugins="plugins"
      :css-classes="cssClasses"
      :styles="styles"
      :width="width"
      :height="height"
    />
  </template>
  
  <script>
  import { Doughnut } from 'vue-chartjs'
  import axios from 'axios';

  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    CategoryScale
  } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)
  
  export default {
    name: 'DoughnutChart',
    components: {
      Doughnut
    },
    props: {
      chartId: {
        type: String,
        default: 'doughnut-chart'
      },
      datasetIdKey: {
        type: String,
        default: 'label'
      },
      width: {
        type: Number,
        default: 400
      },
      height: {
        type: Number,
        default: 400
      },
      cssClasses: {
        default: '',
        type: String
      },
      styles: {
        type: Object,
        default: () => {}
      },
      plugins: {
        type: Array,
        default: () => []
      }
    },
    data() {
      return {
        chartData: {
            labels: [],
            datasets: [
            {
              backgroundColor: ['#ff9c9c', '#ffd1fd','#ffbf9c', '#ffe89c', '#b3ff9c', '#9cefff', '#9cc0ff', '#ab9cff', '#dc9cff'],
              data: []
            }
          ]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false
        }
      }
    },
    created () {
        axios.get('http://localhost:3100/rent_data')
        .then(response => {
            this.chartData.labels = response.data.county_;
            this.chartData.datasets[0].data = response.data.totalProduction_;
            return true;
        })
        .catch(error => console.log(error));
    }
  }
  </script>