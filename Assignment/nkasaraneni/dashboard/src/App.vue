<script lang="ts">
// import StackedDataExample from './components/StackedData-- example data.vue'
// import StackedDataExampleInteractive from './components/StackedData-- example data interactive.vue'
// import StackedData from './components/StackedData-- my data.vue'
// import StackedDataInteractive from './components/StackedData-- my data interactive.vue'
import LineDataInteractive from './components/LineData.vue'
import ParallelData from './components/ParallelData.vue'


export default {
  components: {
    // StackedDataExample,
    // StackedDataExampleInteractive,
    // StackedData,
    // StackedDataInteractive,
    LineDataInteractive,
    ParallelData
  }
}
</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
    <v-row no-gutters>
      <v-col cols="5">
        <LineDataInteractive/>
      </v-col>
      <v-col cols="5">
        <ParallelData/>
      </v-col>
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
  height: 100%;
}
</style>
