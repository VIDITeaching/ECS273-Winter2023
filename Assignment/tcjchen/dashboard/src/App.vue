<script lang="ts">
import BarWithInteractions from './components/BarWithInteractions.vue';
import WordCloudInteractions from './components/WordCloudWithInteractions.vue';

export default {
  components: {
    BarWithInteractions,
    WordCloudInteractions,
  }
}
</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
    <v-row no-gutters>
      <v-col cols="6">
        <WordCloudInteractions />
      </v-col>
      <v-col cols="6">
        <BarWithInteractions />
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="5">
      </v-col>
      <v-col cols="5">

      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
#main-container {
  height: 100%;
  background-color: antiquewhite;
}
</style>
