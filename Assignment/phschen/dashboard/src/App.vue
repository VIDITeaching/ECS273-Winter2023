<script lang="ts">
import Notes from './components/Notes.vue'
import Example from './components/Example.vue'
import ExampleWithLegend from './components/ExampleWithLegend.vue';
import ExampleWithInteractions from './components/ExampleWithInteractions.vue';
import Bar from './components/Bar.vue';
import Line from './components/Line.vue';
import PieChart from './components/PieChart.vue';
import Doughnut from './components/Doughnut.vue';

export default {
  components: {
    Notes,
    Example,
    ExampleWithLegend,
    ExampleWithInteractions,
    Bar,
    Line,
    PieChart,
    Doughnut
  },
  data() {
    return {
      selectedOption: 'option1',
      options: [
        { value: 'option1', text: 'Pie Chart' },
        { value: 'option2', text: 'Doughnut Chart' }
      ]
    }
  }
}
</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
    <v-row no-gutters>
      <v-col cols="5">
        <Bar/>
      </v-col>
      <v-col cols="5">
        <div><h3>Please select Pie Chart/Doughtnut Chart:</h3>
        <select class="dropdown-option" v-model="selectedOption">
          <option v-for="option in options" :value="option.value">{{ option.text }}</option>
        </select>
        <PieChart v-if="selectedOption === 'option1'"></PieChart>
        <Doughnut v-else></Doughnut>
      </div>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <!-- <Notes msg="This message is showcasing how to pass down the props"/> -->
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
#main-container{
  height: 100%;
}
.dropdown-option {
  font-size: 36px;
  font-weight: bold;
}
</style>