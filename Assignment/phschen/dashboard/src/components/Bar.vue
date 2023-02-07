<template>
    <h1>Bar Chart</h1>
    <h2>Total production of housing in each county</h2>
    <!-- <h5>{{ chartData }}</h5>
    <h5>{{chartData.labels}}</h5>
    <h5>{{chartData.datasets[0].datas}}</h5> -->
    <Bar
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
  import { Bar } from 'vue-chartjs'
  import axios from 'axios';
  
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
  } from 'chart.js'

  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  export default {
    name: 'BarChart',
    components: {
      Bar
    },
    props: {
      chartId: {
        type: String,
        default: 'bar-chart'
      },
      datasetIdKey: {
        type: String,
        default: 'label'
        // default: 'name'
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

    data () {
        return {
            chartData: {
                labels: [],
                datasets: [
                    {
                        label: 'Total production of housing',
                        backgroundColor: '#59cbff',
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
        // axios.get(`${server}/cal_csv`)
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