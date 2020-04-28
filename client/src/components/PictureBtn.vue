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
    <svg v-if="url != null" height="100%" width="100%" viewBox="0 0 1599 1200">
      <image height="100%" width="100%" :xlink:href="url"></image>
      <path
        v-for="(path, index) in paths"
        :key="index"
        :d="path.d"
        :class="GetClass(path.type)"
        @click="OpenDialog(path.type)"
      />
    </svg>
    <v-label v-if="url != null">{{ url }}</v-label>
    <plants-list-modal :dialog="dialog" :type="selectedType" :plants="plants" />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import Axios from "axios";
import * as firebase from "firebase/app";
import "firebase/storage";
import PlantsListModal from "./PlantsListModal.vue";
export default Vue.extend({
  components: {
    PlantsListModal
  },
  data: () => ({
    dialog: false as boolean,
    selectedType: null as null | string,
    picture: "" as string,
    paths: [] as Array<object>,
    progress: 0 as number,
    showProgress: false as boolean,
    url: null as null | string,
    plants: null as null | Array<object>
  }),
  created() {
    this.$root.$on("CloseDialog", () => {
      this.dialog = false;
    });
  },
  computed: {
    Progress(): number {
      return Math.round(this.progress);
    }
  },
  methods: {
    OpenDialog(type: string): void {
      this.selectedType = type;
      this.dialog = true;
    },
    GetClass(type: string): string {
      switch (type) {
        case "Low":
          return "path-low";
        case "Medium":
          return "path-med";
        case "High":
          return "path-high";
        default:
          return "path-med";
      }
    },
    Clear(): void {
      this.selectedType = null;
      this.picture = "";
      this.paths = [];
      this.progress = 0;
      this.url = null;
      this.plants = null;
    },
    Upload(image: File): void {
      this.Clear();
      this.showProgress = true;
      const storageRef = firebase
        .storage()
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
            Axios.post(`${process.env.VUE_APP_SERVER_URL}/analyze`, {
              id: 1,
              // eslint-disable-next-line @typescript-eslint/camelcase
              pic_url: url
            }).then(response => {
              this.paths = response.data.svg;
              this.plants = response.data.plants;
            });
          });
        }
      );
    }
  }
});
</script>

<style scoped>
path {
  fill: transparent;
  transition: 1s;
  stroke-width: 1;
  opacity: 1;
  cursor: pointer;
}

.path-low {
  stroke: darkgreen;
}
.path-med {
  stroke: green;
}
.path-high {
  stroke: lightgreen;
}

.path-low:hover {
  fill: darkgreen;
  opacity: 0.7;
}
.path-med:hover {
  fill: green;
  opacity: 0.7;
}
.path-high:hover {
  fill: lightgreen;
  opacity: 0.7;
}
</style>
