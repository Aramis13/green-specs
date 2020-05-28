import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import * as firebase from "firebase/app";
import "firebase/analytics";

// Your web app's Firebase configuration
const firebaseConfig = process.env.VUE_APP_FIREBASECONFIG;

// Initialize Firebase
firebase.initializeApp(JSON.parse(firebaseConfig));
firebase.analytics();

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
