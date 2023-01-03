<script lang="ts">
import { useExampleStore } from '../stores/exampleStore';
import { watch } from 'vue';

export default {
  setup() {
    const store = useExampleStore()
    // This is the state read from store
    // This is showing how the store update from one component will also be reflected in other components
    watch(store, (state) => { 
      console.log(state.size)
    })
    return {
      count: 0 // This is the local state of this component
    }
  },
  props: {
    msg: String, // This is the props passed down from the parent component
  },
}
</script>

<!-- The following is showcasing how to use UI components from Vuetify-->
<template>
  <h3 class="ma-2">{{ msg }}</h3>

  <v-divider class="pt-1 pb-1"/>

  <v-card class="ma-2 pa-4">
    <p class="pb-1">
      Edit
      <code>components/Notes.vue</code> to try different UI components from Vuetify
    </p>

    <v-card-text>
      Note that this template uses Vuetify 3, where the hyperlinks in their current documentation are messed up (as they all are linked to Japanese translation, which is currently not available). ¯\_(ツ)_/¯ <br />
      You may either go check out the doc for <a href="https://vuetifyjs.com/en/">Vuetify 2</a>, or fix the hyperlink by changing the language. <br />
      For example, "https://next.vuetifyjs.com/<strong>ja</strong>/api/v-card/" won't work, but "https://next.vuetifyjs.com/<strong>en</strong>/api/v-card/" works.
    </v-card-text>

    <v-btn @click="count++" elevation="2">
      Have clicked this {{ count }} times
    </v-btn>
  </v-card>

</template>

<style scoped>
</style>
