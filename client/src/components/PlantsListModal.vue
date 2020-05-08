<template>
  <v-dialog
    v-model="dialog"
    :fullscreen="$vuetify.breakpoint.xs"
    :max-width="$vuetify.breakpoint.xs ? '' : '800'"
    dark
    no-click-animation
  >
    <v-card class="hide-overflow">
      <v-list-item>
        <v-btn icon @click="Alert" class="mr-3">
          <v-icon color="primary" large>mdi-information-outline</v-icon></v-btn
        >
        <v-list-item-content>
          <v-list-item-title class="headline">{{
            plants[plantIndex].nickname
          }}</v-list-item-title>
          <v-list-item-subtitle>{{
            plants[plantIndex].Name
          }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn icon @click="Close"
            ><v-icon>mdi-close</v-icon></v-btn
          ></v-list-item-action
        >
      </v-list-item>

      <v-carousel
        hide-delimiters
        @change="PlantChange"
        transition="fade-transition"
        :height="$vuetify.breakpoint.xs ? '100%' : '500px'"
      >
        <v-carousel-item v-for="(plant, index) in dummyPlants" :key="index">
          <v-img
            :src="plant"
            width="100%"
            height="100%"
            :contain="$vuetify.breakpoint.xs ? false : true"
          ></v-img>
        </v-carousel-item>
      </v-carousel>

      <v-card-actions class="justify-space-around">
        <v-list>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                class="title"
                v-text="'Involvement:'"
              ></v-list-item-title>
            </v-list-item-content>
            <v-list-item-action
              ><v-rating
                color="brown"
                background-color="secondary"
                full-icon="mdi-shovel"
                empty-icon="mdi-shovel"
                :value="3"
                readonly
              ></v-rating
            ></v-list-item-action>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                class="title"
                v-text="'Size:'"
              ></v-list-item-title>
            </v-list-item-content>
            <v-list-item-action
              ><v-rating
                color="accent"
                background-color="secondary"
                full-icon="mdi-tree"
                empty-icon="mdi-tree-outline"
                :value="1"
                readonly
              ></v-rating
            ></v-list-item-action>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                class="title"
                v-text="'Price:'"
              ></v-list-item-title>
            </v-list-item-content>
            <v-list-item-action
              ><v-rating
                color="green darken-4"
                background-color="secondary"
                full-icon="mdi-currency-usd-circle"
                empty-icon="mdi-currency-usd-circle-outline"
                :value="4"
                readonly
              ></v-rating
            ></v-list-item-action>
          </v-list-item>
        </v-list>
      </v-card-actions>
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
    Alert(): void {
      alert("To Be Continued...");
    },
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
