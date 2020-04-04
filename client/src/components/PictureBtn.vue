<template>
  <v-container>
    <v-file-input
      show-size
      accept="image/*"
      label="Take Picture"
      prepend-icon="mdi-camera"
      @change="Upload"
    ></v-file-input>
    <v-layout v-if="showProgress" d-flex justify-center mt-12 display-1>
      <v-progress-circular
        rotate="-90"
        color="primary"
        size="300"
        width="20"
        :value="progress"
        >{{ Progress }}</v-progress-circular
      >
    </v-layout>
    <v-img :src="picture"></v-img>
    <v-label v-if="url != null">{{ url }}</v-label>
  </v-container>
</template>

<script>
import Vue from "vue";
// import Axios from "axios";
import * as firebase from "firebase/app";
import 'firebase/storage'
export default Vue.extend({
  data: () => ({
    picture: "",
    progress: 0,
    showProgress: false,
    url: null
  }),
  computed: {
    Progress() {
      return Math.round(this.progress);
    }
  },
  methods: {
    Upload(image) {
      this.showProgress = true;

      const storageRef = firebase.storage()
        .ref(image.name)
        .put(image);
      storageRef.on(
        `state_changed`,
        snapshot => {
          this.progress =
            (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        },
        error => {
          console.log(error.message);
          alert(error.message);
        },
        () => {
          storageRef.snapshot.ref.getDownloadURL().then(url => {
            this.picture = url;
            this.url = url;
            this.showProgress = false;
            // Send url to server
          });
        }
      );
    }
  }
});
</script>

<style scoped></style>
