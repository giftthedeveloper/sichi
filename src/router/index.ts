import { createRouter, createWebHistory } from 'vue-router';

import ChatView from '../views/ChatView.vue';
import DashboardView from '../views/DashboardView.vue';
import TransactionsView from '../views/TransactionsView.vue';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard', component: DashboardView },
    { path: '/chat', name: 'chat', component: ChatView },
    { path: '/transactions', name: 'transactions', component: TransactionsView }
  ]
});
