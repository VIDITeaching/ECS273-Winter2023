<script lang="ts">
import BeanVIS1 from './components/BeanVIS1.vue';
import BeanVIS2 from './components/BeanVIS2.vue';
import Notes from './components/Notes.vue'
import Example from './components/Example.vue'
import ExampleWithLegend from './components/ExampleWithLegend.vue';
import ExampleWithInteractions from './components/ExampleWithInteractions.vue';

export default {
  components: {
    BeanVIS1,
    BeanVIS2,
    Notes,
    Example,
    ExampleWithLegend,
    ExampleWithInteractions
  }
}
</script>

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
    <v-row no-gutters>
      <v-col cols="6">
        <BeanVIS1/>
      </v-col>
      <v-col cols="6">
        <BeanVIS2/>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
#main-container{
  height: 100%;
}
</style>
