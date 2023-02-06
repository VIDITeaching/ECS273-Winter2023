<script lang='ts'>
import Notes from './components/Notes.vue'
import Example from './components/Example.vue'
import ExampleWithLegend from './components/ExampleWithLegend.vue';
import ExampleWithInteractions from './components/ExampleWithInteractions.vue';
import Chart from './components/Chart.vue'
import Parallel from './components/Parallel.vue'

export default {
  components: {
    // Parallel,
    Chart,
    Notes,
    Example,
    ExampleWithLegend,
    ExampleWithInteractions
  }
}
</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id='main-container' class='d-flex flex-column flex-nowrap' fluid>
    <v-row no-gutters>
      <v-col cols='12'>
        <Chart />
      </v-col>
      <!-- <v-col cols='5'>
        <Example />
      </v-col> -->
    </v-row>
    <v-row no-gutters>
      <v-col>
        <!-- <Notes msg='This message is showcasing how to pass down the props'/> -->
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
#main-container{
  height: 100%;
}
</style>
