<script lang="ts">

import ScatterPlot_Fashion_Mnist from './components/ScatterPlot_Fashion_Mnist.vue';
import LinePlot_mnist_with_interaction from './components/LinePlot_mnist_with_interaction.vue';
export default {
  components: {
    ScatterPlot_Fashion_Mnist,
    LinePlot_mnist_with_interaction
  }
}
</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id="main-container" class="d-flex flex-column flex-nowrap " fluid>
    <v-row  no-gutters>
      <v-col style="width: 50%;">
        <LinePlot_mnist_with_interaction/>
      </v-col>
      <v-col cols="6">
        <ScatterPlot_Fashion_Mnist/>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
#main-container{
  height: 100%;
}
</style>
