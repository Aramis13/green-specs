<template>
  <v-dialog
    v-model="dialog"
    :fullscreen="$vuetify.breakpoint.xs"
    :max-width="$vuetify.breakpoint.xs ? '' : '800'"
    dark
    no-click-animation
  >
    <v-card class="hide-overflow">
      <v-card-title
        >{{ plant.nickname }}<v-spacer /><v-btn icon @click="Close"
          ><v-icon>mdi-close</v-icon></v-btn
        ></v-card-title
      >
      <v-divider />
      <v-card-text
        ><span class="title">{{ plant.Story }}</span>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  props: ["dialog", "plant"],
  methods: {
    Close(): void {
      this.$root.$emit("ClosePlantInfo");
    },
  },
});
</script>

<style scoped>
.hide-overflow {
  overflow: hidden;
}
</style>
