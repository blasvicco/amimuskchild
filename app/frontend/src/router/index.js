// Libs imports
import { createRouter, createWebHistory } from 'vue-router';

// Views imports
import main from '@/views/main.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [{
    path: '/',
    name: 'main',
    component: main,
  }],
});

export default router;
