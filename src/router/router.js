import { createRouter, createWebHashHistory } from "vue-router";
import HelloWorldVue from "../components/HelloWorld.vue";
import Login from "../components/Login.vue";
import Dashboard from "../components/Dashboard.vue";

const routes = [
  { path: "/", component: HelloWorldVue, name: "base" },
  { path: "/login", component: Login, name: "Login" },
  { path: "/dashboard", component: Dashboard, name: "Dashboard" },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});
