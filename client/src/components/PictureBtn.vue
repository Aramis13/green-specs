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
export default Vue.extend({
  data: () => ({
    picture: "",
    loading: false
  }),
  methods: {
    Upload(image) {
      this.loading = true;
      const fr = new FileReader();

      fr.readAsDataURL(image);

      fr.onload = e => {
        if (e == null || e.target == null) return;
        this.picture = e.target.result;
      };

      const formData = new FormData();
      formData.append("image", image, image.name);
      Axios.post("/healthcheck", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
        .then(response => {
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
});
</script>

<style scoped></style>
