import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/home.vue'
import Company from '../components/company.vue'
import Create from '../components/create.vue'
import NewFY from '../components/newFY.vue'
import Modify from '../components/modify.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/Company',
      name: "Company",
      component: Company
    },
    {
      path: '/create',
      name: 'Create',
      component: Create
    },
    {
      path: '/newFY',
      name: 'New F.Y.',
      component: NewFY
    },
    {
      path: '/modify',
      name: 'Modify',
      component: Modify
    },
  ]
})

export default router
