<template>
    <!-- <h4>{{ chartData.labels }}</h4> -->
    <h4>Line Chart</h4>
    <h5>This chart shows average number of months that the terrorism occurs in each year.</h5>
    <LineChartGenerator
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
  import { Line as LineChartGenerator } from 'vue-chartjs'
  import axios from 'axios';
  import { server } from '../helper';
  
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    CategoryScale,
    PointElement
  } from 'chart.js'
  
  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    CategoryScale,
    PointElement
  )
  
  export default {
    name: 'LineChart',
    components: {
      LineChartGenerator
    },
    props: {
      chartId: {
        type: String,
        default: 'line-chart'
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
              label: 'Average number of months in which the terrorism occurred',
              backgroundColor: '#c3e69a',
              data: []
            }
          ]
        },
        chartOptions: { 
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: "Year",
                color: "#787878",
                font: {
                  size: 16,
                  weight: "bold"
                }
              }
            },
            y: {
              title: {
                display: true,
                text: "Number of months",
                color: "#787878",
                font: {
                  size: 16,
                  weight: "bold"
                }
              }
            }
          }
        }
      }
    },
    created () {
        axios.get(`${server}/fetchExample`)
        .then(resp => {
            this.chartData.labels = resp.data.labels;
            this.chartData.datasets[0].data = resp.data.monthCount;
            return true;
        })
        .catch(error => console.log(error));
    }
  }
  </script>