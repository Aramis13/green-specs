<template>
  <v-app>
    <v-parallax src="./assets/background.jpg" class="wallpaper pa-0">
      <v-content>
        <v-container fill-height fluid pa-0 ma-0>
          <v-btn
            color="primary"
            v-if="updateExists"
            @click="refreshApp"
            fixed
            top
            right
            ><v-icon left>mdi-update</v-icon>Update</v-btn
          >
          <div v-if="updateExists">This is a test</div>
          <router-view></router-view>
        </v-container>
      </v-content>
    </v-parallax>
  </v-app>
</template>

<script>
import Vue from "vue";
export default Vue.extend({
  name: "App",

  data() {
    return {
      refreshing: false,
      registration: null,
      updateExists: false
    };
  },

  created() {
    // Listen for swUpdated event and display refresh snackbar as required.
    document.addEventListener("swUpdated", this.showRefreshUI, { once: true });
    // Refresh all open app tabs when a new service worker is installed.
    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (this.refreshing) return;
      this.refreshing = true;
      window.location.reload();
    });
  },
  methods: {
    showRefreshUI(e) {
      // Display a button inviting the user to refresh/reload the app due
      // to an app update being available.
      // The new service worker is installed, but not yet active.
      // Store the ServiceWorkerRegistration instance for later use.
      this.registration = e.detail;
      this.updateExists = true;
    },
    refreshApp() {
      // Handle a user tap on the update app button.
      this.updateExists = false;
      // Protect against missing registration.waiting.
      if (!this.registration || !this.registration.waiting) {
        return;
      }
      this.registration.waiting.postMessage("skipWaiting");
    }
  }
});
</script>

<style>
html {
  overflow-y: auto !important;
}
.wallpaper {
  height: 100% !important;
  width: inherit;
}
.v-parallax__content {
  padding: 0 !important;
}
</style>
