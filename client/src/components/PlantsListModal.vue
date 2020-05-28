<template>
  <div>
    <v-dialog
      v-model="dialog"
      :fullscreen="$vuetify.breakpoint.xs"
      :max-width="$vuetify.breakpoint.xs ? '' : '800'"
      dark
      no-click-animation
    >
      <v-card class="hide-overflow">
        <v-list-item class="px-2">
          <v-btn icon class="mr-3" link @click="OpenPlantUrl">
            <v-icon color="primary" large
              >mdi-information-outline</v-icon
            ></v-btn
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

        <v-card-text class="px-2 py-2">
          <v-carousel
            hide-delimiters
            @change="PlantChange"
            transition="fade-transition"
          >
            <v-carousel-item
              v-for="(plant, index) in plants"
              :key="index"
              :src="plant['Picture URL']"
            >
            </v-carousel-item>
          </v-carousel>
        </v-card-text>
        <v-card-actions>
          <v-row justify="center">
            <template v-for="tag in tags">
              <v-tooltip top :key="`tooltip${tag}`">
                <template v-slot:activator="{ on }">
                  <v-chip
                    :key="tag"
                    class="mx-1"
                    color="primary darken-1"
                    v-on="on"
                  >
                    <v-icon :key="`${tag}-icon`">{{ tag }}</v-icon>
                  </v-chip>
                </template>
                <span>{{ tagMeta[tag] }}</span>
              </v-tooltip>
            </template>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <plant-info :dialog="plantInfoDialog" :plant="selectedPlant" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import PlantInfo from "./PlantInfo.vue";
export default Vue.extend({
  props: ["dialog", "type", "plants"],
  components: {
    PlantInfo,
  },
  data: () => ({
    tags: [] as Array<string>,
    tagMeta: {
      "mdi-sovel": "DIY",
      "food-apple": "Edible",
      "mdi-skull-crossbones": "Danger",
      "mdi-leaf": "Special leafs",
      "mdi-flower": "Special Flowers",
    },
    dummyPlants: [] as Array<string>,
    plantIndex: 0 as number,
    plantInfoDialog: false as boolean,
    selectedPlant: {} as null | Record<string, unknown>,
  }),
  created() {
    this.$root.$on("ClosePlantInfo", () => {
      this.plantInfoDialog = false;
    });
  },
  methods: {
    OpenPlantUrl(): void {
      // window.open(this.plants[this.plantIndex]["Plant information link"]);
      this.selectedPlant = this.plants[this.plantIndex];
      this.plantInfoDialog = true;
    },
    PlantChange(index: number): void {
      this.plantIndex = index;
      this.tags = [];
      const plant = this.plants[this.plantIndex];
      if (plant["DIY"]) this.tags.push("mdi-sovel");
      if (plant["Edible"]) this.tags.push("mdi-food-apple");
      if (plant["Warnings"]) this.tags.push("mdi-skull-crossbones");
      if (plant["Special leafs"]) this.tags.push("mdi-leaf");
      if (plant["Special Flowers"]) this.tags.push("mdi-flower");
    },
    Close(): void {
      this.$root.$emit("CloseDialog");
    },
  },
  computed: {
    PlantInfo(): Array<Record<string, unknown>> {
      const info = [];
      for (const key in this.plants[this.plantIndex]) {
        info.push({
          Title: key,
          Data: this.plants[this.plantIndex][key],
        });
      }
      return info;
    },
  },
});
</script>

<style scoped>
.hide-overflow {
  overflow: hidden;
}
</style>
