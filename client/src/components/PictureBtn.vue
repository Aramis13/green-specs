<template>
  <v-row align="center" justify="center">
    <!-- <v-file-input
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
    </v-layout> -->
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
      style="display: none"
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
      v-if="url != null && !showProgress"
      height="100%"
      width="100%"
      :viewBox="ViewBox"
    >
      <image
        preserveAspectRatio="none"
        x="0"
        y="0"
        height="100%"
        width="100%"
        style="overflow: visible;"
        :xlink:href="url"
      ></image>
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
    plants: null as null | Array<object>,
    clicked: false as boolean
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
    ViewBox() {
      return `0 0 ${screen.width} ${screen.height}`;
    }
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
.glasses {
  height: 210;
  width: 210;
}
</style>
