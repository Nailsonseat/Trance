import { createRouter, createWebHashHistory } from "vue-router";
import HelloWorldVue from "../components/HelloWorld.vue";

const routes = [{ path: "/", component: HelloWorldVue }];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});
