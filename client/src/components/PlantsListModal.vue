<template>
  <v-dialog v-model="dialog" max-width="800" persistent>
    <v-card>
      <v-card-title class="headline"
        >Plants In Category - {{ type }}<v-spacer /><v-btn icon @click="Close"
          ><v-icon>mdi-close</v-icon></v-btn
        ></v-card-title
      >
      <v-divider />
      <v-card-text class="title">
        Plant List Goes Below
        <br />
        -
        <br />
        -
        <br />
        -
        <br />
        -
        <br />
        -
        <br />
        -
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ["dialog", "type"],
  methods: {
    Close() {
      this.$parent.dialog = false;
    }
  }
};
</script>
