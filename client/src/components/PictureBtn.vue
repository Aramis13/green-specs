<template>
  <v-row align="center" justify="center">
    <v-btn
      @click="TakePicture"
      fab
      elevation="12"
      height="250"
      width="250"
      outlined
      class="green darken-4"
      v-if="!clicked"
    >
      <v-icon size="200" color="white">mdi-glasses</v-icon>
    </v-btn>
    <input
      type="file"
      style="display: none;"
      ref="image"
      accept="image/*"
      @change="Upload"
      v-if="!clicked"
    />
    <v-progress-circular
      style="border-radius: 50%;"
      rotate="-90"
      class="green darken-4"
      color="white"
      size="250"
      width="20"
      :value="progress"
      v-if="showProgress"
    >
      <v-icon size="200" color="white">mdi-glasses</v-icon></v-progress-circular
    >
    <svg
      style="position: fixed;"
      v-if="url != null && !showProgress"
      height="100%"
      width="100%"
      :viewBox="ViewBox"
    >
      <image :height="height" :width="width" :xlink:href="url"></image>
      <path
        v-for="(path, index) in paths"
        :key="index"
        :d="path.d"
        :class="GetClass(path.type)"
        @click="OpenDialog(path.type)"
      />
    </svg>
    <plants-list-modal
      v-if="plants != null"
      :dialog="dialog"
      :type="selectedType"
      :plants="plants"
    />
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import Axios from "axios";
import * as firebase from "firebase/app";
import "firebase/storage";
import PlantsListModal from "./PlantsListModal.vue";
export default Vue.extend({
  components: {
    PlantsListModal,
  },
  data: () => ({
    dialog: false as boolean,
    selectedType: null as null | string,
    picture: "" as string,
    paths: [] as Array<Record<string, unknown>>,
    progress: 0 as number,
    showProgress: false as boolean,
    url: null as null | string,
    plants: null as null | Array<Record<string, unknown>>,
    clicked: false as boolean,
    image: new Image(),
    width: 0 as number,
    height: 0 as number,
  }),
  created() {
    this.$root.$on("CloseDialog", () => {
      this.dialog = false;
    });
  },
  computed: {
    Progress(): number {
      return Math.round(this.progress);
    },
    ViewBox(): string {
      return `0 0 ${this.width} ${this.height}`;
    },
  },
  methods: {
    TakePicture(): void {
      (this.$refs.image as HTMLFormElement).click();
    },
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
    Upload(e: Event): void {
      this.Clear();
      if (!e || !e.target || !(e.target as HTMLFormElement).files) return;
      this.clicked = true;
      const image = (e.target as HTMLFormElement).files[0];
      this.showProgress = true;
      const storageRef = firebase.storage().ref(image.name).put(image);
      storageRef.on(
        `state_changed`,
        (snapshot) => {
          this.progress =
            (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        },
        (error) => {
          console.log(error.message);
          alert(error.message);
        },
        () => {
          storageRef.snapshot.ref.getDownloadURL().then((url) => {
            this.image.src = url;
            if (this.image) {
              this.image.onload = () => {
                this.width = this.image.width;
                this.height = this.image.height;
              };
            }
            this.picture = url;
            this.url = url;
            this.showProgress = false;
            Axios.post(`${process.env.VUE_APP_SERVER_URL}/analyze`, {
              id: 1,
              pic_url: url,
            }).then((response) => {
              this.paths = response.data.svg.svg_paths;
              this.plants = response.data.plants;
            });
          });
        }
      );
    },
  },
});
</script>

<style scoped>
path {
  transition: 1s;
  stroke-width: 1;
  opacity: 0.3;
  cursor: pointer;
}

.path-low {
  fill: red;
  stroke: red;
}
.path-med {
  fill: yellow;
  stroke: yellow;
}
.path-high {
  fill: green;
  stroke: green;
}

.path-low:hover {
  opacity: 0.7;
}
.path-med:hover {
  opacity: 0.7;
}
.path-high:hover {
  opacity: 0.7;
}
.glasses {
  height: 210;
  width: 210;
}
</style>
