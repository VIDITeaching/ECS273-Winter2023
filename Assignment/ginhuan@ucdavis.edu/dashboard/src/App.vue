<script lang="ts">
import USElection from "./components/USElection.vue";
import Piechart from "./components/USElection_Piechart.vue";

export default {
 components: {
  USElection,
  Piechart
 },
};
</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
 <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
    <h1>
        US Election 2020 President Debate
    </h1>
  <v-row no-gutters>
   <v-col cols="5">
    <USElection />
   </v-col>
   <v-col>
    <Piechart/>
   </v-col>
   <!-- <v-col>
    <Barchart/>
   </v-col> -->
  </v-row>
 </v-container>
</template>

<style scoped>
#main-container {
 height: 100%;
}
</style>
