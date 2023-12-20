import "bootstrap/dist/css/bootstrap.css";
import { createApp } from "vue";
import App from "./App.vue";
import { router } from "./router/router.js";
import "bootstrap-icons/font/bootstrap-icons.css";
import uploader from "vue-simple-uploader";
import "./style.css";

// const tokenKey = "auth-token";
// router.beforeEach((to, from, next) => {
//   if (
//     to.name !== "UserAuth" &&
//     to.name !== "CreatorAuth" &&
//     !localStorage.getItem("auth-token")
//   )
//     next({ name: "UserAuth" });
//   else next();
// });

const app = createApp(App);
app.use(router);
app.use(uploader);
app.mount("#app");

import "bootstrap/dist/js/bootstrap.js";
