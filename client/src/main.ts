import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import firebase from "firebase";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBMHdDgObwlQcox8LSMG4eaqn21xkcU0fQ",
  authDomain: "green-specs.firebaseapp.com",
  databaseURL: "https://green-specs.firebaseio.com",
  projectId: "green-specs",
  storageBucket: "green-specs.appspot.com",
  messagingSenderId: "287869015941",
  appId: "1:287869015941:web:4dafc960683103c43316ec",
  measurementId: "G-PFWWSNGN7K"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
