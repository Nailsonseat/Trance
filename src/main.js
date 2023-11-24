import "bootstrap/dist/css/bootstrap.css";

import { createApp } from "vue";
import App from "./App.vue";

import { router } from "./router/router.js";

import "bootstrap-icons/font/bootstrap-icons.css";

import "./style.css";

// router.beforeEach((to, from, next) => {
//   if (to.name !== "UserAuth" && !localStorage.getItem("auth-token") ? true : false)
//     next({ name: "UserAuth" });
//   else next();
// });

const app = createApp(App);
app.use(router);
app.mount("#app");

import "bootstrap/dist/js/bootstrap.js";
