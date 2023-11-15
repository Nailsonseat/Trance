import { createApp } from "vue";
import App from "./App.vue";
import "./style.css";
import { router } from "./router/router.js";

router.beforeEach((to, from, next) => {
  if (to.name !== "Login" && !localStorage.getItem("auth-token") ? true : false)
    next({ name: "Login" });
  else next();
});

const app = createApp(App);
app.use(router);
app.mount("#app");
