import { createRouter, createWebHashHistory } from "vue-router";
import HelloWorldVue from "../components/HelloWorld.vue";
import UserAuth from "../components/UserAuth.vue";
import CreatorAuth from "../components/CreatorAuth.vue";
import AdminAuth from "../components/AdminAuth.vue";
import Dashboard from "../components/Dashboard.vue";
import UserHome from "../components/UserHome.vue";
import CreatorHome from "../components/CreatorHome.vue";

const routes = [
  { path: "/", component: HelloWorldVue, name: "base" },
  { path: "/login", component: UserAuth, name: "UserAuth" },
  { path: "/login-c", component: CreatorAuth, name: "CreatorAuth" },
  { path: "/admin-auth", component: AdminAuth, name: "AdminAuth" },
  { path: "/dashboard", component: Dashboard, name: "Dashboard" },
  { path: "/home-user", component: UserHome, name: "UserHome" },
  { path: "/home-creator", component: CreatorHome, name: "CreatorHome" },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});
