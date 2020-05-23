module.exports = {
  transpileDependencies: ["vuetify"],
  pwa: {
    workboxPluginMode: "InjectManifest",
    workboxOptions: {
      swSrc: "./src/sw.js",
      swDest: "service-worker.js"
    },
    name: "Green Specs",
    themeColor: "#1B5E20",
    appleMobileWebAppCapable: "yes"
  }
};
