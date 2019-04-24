<template>
  <v-container>
    <v-layout text-xs-center wrap>
      <v-flex mb-4>
        <h3 class="display-2 font-weight-bold mb-3">
          <vue-dropzone
            ref="myVueDropzone"
            id="dropzone"
            :options="dropzoneOptions" 
          >Drop your image here</vue-dropzone>
        </h3>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
/* eslint-disable */
import vue2Dropzone from "vue2-dropzone";
import "vue2-dropzone/dist/vue2Dropzone.min.css";
export default {
  name: "DropZone",
  data() {
    return {
      dropzoneOptions: {
        url: "https://httpbin.org/post"
      }
    };
  },
  components: {
    vueDropzone: vue2Dropzone
  },
  methods: {
    // dropzoneOptions: {
    //   url: "https://httpbin.org/post",
    //   thumbnailWidth: 150,
    //   maxFilesize: 0.5,
    //   headers: { "My-Awesome-Header": "header value" }
    // }
  }
};
</script>

<style>
</style>
