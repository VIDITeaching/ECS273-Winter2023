<template>
    <h4>Radar Chart</h4>
    <h5>This chart shows the number of terrorisom events and successful terrorisom events of different countries.</h5>
    <!-- <h4>{{ chartData.datasets[1].data }}</h4> -->
    <Radar
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
  import { Radar } from 'vue-chartjs'
  import axios from 'axios';
  import { server } from '../helper';

  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    PointElement,
    LineElement,
    RadialLinearScale
  } from 'chart.js'
  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    PointElement,
    RadialLinearScale,
    LineElement
  )
  export default {
    name: 'RadarChart',
    components: {
      Radar
    },
    props: {
      chartId: {
        type: String,
        default: 'radar-chart'
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
            //   labels: ['Eating','Drinking','Sleeping','Designing','Coding','Cycling','Running','coding'],
            labels: [],
            datasets: [
                {
                    label: 'Number of terrorisom events',
                    backgroundColor: 'rgba(242, 204, 109, 0.2)',
                    borderColor: 'rgb(242, 204, 109)',
                    pointBackgroundColor: 'rgb(242, 204, 109)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(242, 204, 109)',
                    data: []
                },
                {
                    label: 'Number of success terrorisom events',
                    backgroundColor: 'rgba(242, 125, 109, 0.2)',
                    borderColor: 'rgba(242, 125, 109, 1)',
                    pointBackgroundColor: 'rgba(242, 125, 109, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(242, 125, 109, 1)',
                    data: []
                }
            ]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            zoom: {
              animation: {
                duration: 1000,
                easing: 'easeOutCubic'
              }
            }
          }
        }
      }
    },
    created () {
        axios.get(`${server}/fetchExample`)
        .then(resp => {
            this.chartData.labels = resp.data.countryName;
            this.chartData.datasets[0].data = resp.data.countryCount;
            this.chartData.datasets[1].data = resp.data.countryCountSuccess;
            return true;
        })
        .catch(error => console.log(error));
    }
  }
  </script>