<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Eagle Eye</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>

    </v-toolbar>

    <v-content>
      <HelloWorld/>
      <Dropzone/>
    </v-content>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld'
import Dropzone from './components/DropZone'

export default {
  name: 'App',
  components: {
    HelloWorld,
    Dropzone
  },
  data () {
    return {
      //
    }
  }
}
</script>
