<script lang="ts">
import BarPlot from "./components/BarPlot.vue";
import ScatterPlot from "./components/ScatterPlot.vue";

export default {
  components: {
    ScatterPlot,
    BarPlot
  }
}
</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
    <v-row no-gutters>
      <v-col style="width: 50%">
        <BarPlot/>
      </v-col>
      <v-col style="width: 50%">
        <ScatterPlot/>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
#main-container{
  height: 100%;
}
</style>
