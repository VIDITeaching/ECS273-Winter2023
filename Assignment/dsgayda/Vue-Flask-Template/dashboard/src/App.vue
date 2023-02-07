<script lang="ts">
import Notes from './components/Notes.vue'
import Example from './components/Example.vue'
import ExampleWithLegend from './components/ExampleWithLegend.vue';
import ExampleWithInteractions from './components/ExampleWithInteractions.vue';
import ParallelCoords from './components/ParallelCoords.vue';
import Rent from './components/Rent.vue';
import Sankey from './components/Sankey.vue';
import Controls from './components/Controls.vue';
import StackedChart from './components/StackedChart.vue';
import BubbleMap from './components/BubbleMap.vue';

export default {
  components: {
    Notes,
    Example,
    ExampleWithLegend,
    ExampleWithInteractions,
    Rent,
    ParallelCoords,
    Sankey,
    Controls,
    StackedChart,
    BubbleMap
  }
};

</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
    <v-row no-gutters>
      <v-col cols="5">
        <BubbleMap/>
      </v-col>
      <!-- <v-col cols="5">
        <ParallelCoords/>
      </v-col> -->
      <v-col cols="5">
        <StackedChart id="stack"/>
      </v-col>

<!-- 
      <v-col cols="5"> 
        <Sankey/>
      </v-col> -->
    </v-row>
    <v-row no-gutters>
      <v-col>
        <Notes msg="This message is showcasing how to pass down the props"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
#main-container{
  height: 100vh;
}


</style>
