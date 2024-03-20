import { createRouter, createWebHashHistory } from "vue-router";
import HelloWorldVue from "../pages/HelloWorld.vue";
import UserAuth from "../pages/user/UserAuth.vue";
import CreatorAuth from "../pages/creator/CreatorAuth.vue";
import AdminAuth from "../pages/admin/AdminAuth.vue";
import Dashboard from "../pages/Dashboard.vue";
import UserHome from "../pages/user/UserHome.vue";
import CreatorHome from "../pages/creator/CreatorHome.vue";
import Unauthorized from "../pages/Unauthorized.vue";
import Test from "../pages/Test.vue";

const routes = [
  { path: "/", redirect: "/login-user" },
  { path: "/login-user", component: UserAuth, name: "UserAuth" },
  { path: "/login-creator", component: CreatorAuth, name: "CreatorAuth" },
  { path: "/admin-auth", component: AdminAuth, name: "AdminAuth" },
  { path: "/dashboard", component: Dashboard, name: "Dashboard" },
  { path: "/unauthorized", component: Unauthorized, name: "Test" },
  {
    path: "/home-user",
    component: UserHome,
    name: "UserHome",
    meta: { requiresUser: true },
  },
  {
    path: "/home-creator",
    component: CreatorHome,
    name: "CreatorHome",
    meta: { requiresCreator: true },
  },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});
