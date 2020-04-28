<template>
  <v-dialog v-model="dialog" fullscreen>
    <v-card class="hide-overflow">
      <v-card-title class="headline"
        >Plants In Category - {{ type }}<v-spacer /><v-btn icon @click="Close"
          ><v-icon>mdi-close</v-icon></v-btn
        ></v-card-title
      >
      <v-divider />
      <v-card-text>
        <v-row>
          <v-col cols="5">
            <v-carousel hide-delimiters @change="PlantChange">
              <v-carousel-item
                v-for="(plant, index) in dummyPlants"
                :key="index"
              >
                <v-img :src="plant" width="100%" height="100%"></v-img>
              </v-carousel-item>
            </v-carousel>
          </v-col>
          <v-col cols="7" v-if="plants != null">
            <v-toolbar
              class="primary--text text-uppercase d-flex justify-center"
              flat
              ><v-toolbar-title class="display-1 font-weight-bold">{{
                plants[plantIndex].Name
              }}</v-toolbar-title></v-toolbar
            >
            <v-list>
              <v-list-item
                v-for="(info, i) in PlantInfo"
                :key="i"
                class="title"
              >
                <v-list-item-content>
                  <v-list-item-title
                    class="text-uppercase title"
                    v-text="`${info.Title}:`"
                  ></v-list-item-title>
                </v-list-item-content>
                <v-list-item-action-text
                  class="title"
                  v-text="info.Data"
                ></v-list-item-action-text>
              </v-list-item>
            </v-list>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  props: ["dialog", "type", "plants"],
  data: () => ({
    dummyPlants: [] as Array<string>,
    plantIndex: 0 as number
  }),
  created() {
    this.dummyPlants.push(
      "https://firebasestorage.googleapis.com/v0/b/green-specs.appspot.com/o/78680062-afcc2880-78f3-11ea-9ef6-58f449f0f0e9.jpg?alt=media&token=7ab4fa76-3125-4716-b824-56ec0253c131"
    );
    this.dummyPlants.push(
      "https://firebasestorage.googleapis.com/v0/b/green-specs.appspot.com/o/78680065-b0fd5580-78f3-11ea-96b3-4b10af69a73f.jpg?alt=media&token=9984703e-4b2e-4ccc-a70f-f10c9f72b5ca"
    );
    this.dummyPlants.push(
      "https://firebasestorage.googleapis.com/v0/b/green-specs.appspot.com/o/78680068-b22e8280-78f3-11ea-8b4b-b79bd5e50f8f.jpg?alt=media&token=5e996da8-2511-4a78-a4b4-c6de631a82f5"
    );
  },
  methods: {
    PlantChange(index: number): void {
      this.plantIndex = index;
    },
    Close(): void {
      this.$root.$emit("CloseDialog");
    }
  },
  computed: {
    PlantInfo() {
      const info = [];
      for (const key in this.plants[this.plantIndex]) {
        info.push({
          Title: key,
          Data: this.plants[this.plantIndex][key]
        });
      }
      return info;
    }
  }
});
</script>

<style scoped>
.hide-overflow {
  overflow: hidden;
}
</style>
