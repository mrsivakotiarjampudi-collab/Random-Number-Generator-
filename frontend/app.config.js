// Load environment variables from .env file
require('dotenv').config();

module.exports = {
  expo: {
    name: process.env.EXPO_APP_NAME || "Random Number Generator",
    slug: process.env.EXPO_APP_SLUG || "random-number-generator",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/images/icon.png",
    scheme: "random-number-generator",
    userInterfaceStyle: "automatic",
    newArchEnabled: true,
    ios: {
      supportsTablet: true
    },
    android: {
      adaptiveIcon: {
        foregroundImage: "./assets/images/adaptive-icon.png",
        backgroundColor: "#000"
      },
      edgeToEdgeEnabled: true
    },
    web: {
      bundler: "metro",
      output: "static",
      favicon: "./assets/images/favicon.png"
    },
    plugins: [
      "expo-router",
      [
        "expo-splash-screen",
        {
          image: "./assets/images/splash-icon.png",
          imageWidth: 200,
          resizeMode: "contain",
          backgroundColor: "#000"
        }
      ]
    ],
    experiments: {
      typedRoutes: true
    },
    extra: {
      EXPO_PUBLIC_BACKEND_URL: process.env.EXPO_PUBLIC_BACKEND_URL,
      EXPO_PACKAGER_HOSTNAME: process.env.EXPO_PACKAGER_HOSTNAME,
      EXPO_PACKAGER_PROXY_URL: process.env.EXPO_PACKAGER_PROXY_URL,
    }
  }
};
