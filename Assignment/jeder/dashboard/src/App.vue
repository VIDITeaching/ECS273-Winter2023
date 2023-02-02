<script lang="ts">
import Overview from './components/Overview.vue';
import Detail1 from './components/Detail1.vue';
import Settings from './components/Settings.vue';
import { useTerrorismDataStore } from './stores/terrorismDataStore';

export default {
  components: {
    Overview,
    Detail1,
    Settings,
  },
  setup() { // Composition API syntax
        const store = useTerrorismDataStore()
        return {
            store, // Return store as the local state, but when you update the property value, the store is also updated.
        }
    },
  created() {
        this.store.fetchTerrorismData()
      
    },
}
</script> 

<!--This is using the grid component from Vuetify to do layout design-->
<template>
  <v-container id="main-container" class="d-flex flex-column flex-nowrap" fluid>
    <v-row no-gutters>
      <v-col>
        <Settings/>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <Overview/>
      </v-col>
      <v-col>
        <Detail1/>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
#main-container{
  height: 100%;
}
</style>
