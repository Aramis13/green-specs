<template>
  <v-app>
    <v-parallax src="./assets/background.jpg" class="wallpaper pa-0">
      <v-content>
        <v-container fill-height fluid pa-0 ma-0>
          <router-view></router-view>
        </v-container>
      </v-content>
    </v-parallax>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  name: "App",

  data: () => ({
    //
  })
});
</script>

<style>
.wallpaper {
  height: 100% !important;
  width: inherit;
}
.v-parallax__content {
  padding: 0 !important;
}
</style>
