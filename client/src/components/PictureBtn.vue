<template>
  <v-container>
    <v-file-input
      :loading="loading"
      show-size
      accept="image/*"
      label="Take Picture"
      prepend-icon="mdi-camera"
      @change="Upload"
    ></v-file-input>

    <v-img :src="picture"></v-img>
  </v-container>
</template>

<script>
import Vue from "vue";
import Axios from "axios";
import Firebase from "firebase";
export default Vue.extend({
  data: () => ({
    picture: "",
    loading: false
  }),
  methods: {
    Upload(image) {
      this.loading = true;

      const storageRef = Firebase.storage()
        .ref(image.name)
        .put(image);
      storageRef.on(
        `state_changed`,
        snapshot => {
          console.log((snapshot.bytesTransferred / snapshot.totalBytes) * 100);
        },
        error => {
          console.log(error.message);
        },
        () => {
          console.log(100);
          storageRef.snapshot.ref.getDownloadURL().then(url => {
            this.picture = url;
            this.loading = false;
            // Send url to server
            Axios.post("/api/image", {
              url: url
            });
          });
        }
      );
    }
  }
});
</script>

<style scoped></style>
