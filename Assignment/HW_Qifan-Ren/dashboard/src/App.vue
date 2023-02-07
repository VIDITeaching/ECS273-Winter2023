<script lang="ts">
import ScatterPlot from './components/ScatterPlot.vue';
import ParallelCoordinates from './components/ParallelCoordinates.vue';

export default {
  data(){
    return {
      index: true as Boolean
    }
  },
  components: {
    ScatterPlot,
    ParallelCoordinates
  },
  methods: {
    changePage(){
      this.index = !this.index
    }
  }
}
</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
    <v-row no-gutters>
      <v-col cols="12">
        <ParallelCoordinates v-if="index === true"/>
        <ScatterPlot v-if="index === false"/>
      </v-col>
    </v-row>
    <br/>
      <v-btn append-icon="mdi-vuetify" @click="changePage">
        Click to see {{index? "scatter plot": "parallel coordinates plot"}}.
      </v-btn>
  </v-container>
</template>

<style scoped>
#main-container{
  height: 100%;
}
</style>
