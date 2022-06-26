import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/login')
  },
  {
    path: '/',
    name: '/',
    component: () => import('../layout'),
    redirect: '/',
    children: [
      {
        path: '/',
        name: 'index',
        component: () => import('@/views/index/index.vue')
      },
      {
        path: 'users',
        name: 'users',
        component: () => import('@/views/users/index.vue')
      },
      {
        path: 'dormitories',
        name: 'dormitories',
        component: () => import('@/views/dormitories/index.vue')
      },
      {
        path: 'buildings',
        name: 'buildings',
        component: () => import('@/views/buildings/index.vue')
      },
      {
        path: 'scores',
        name: 'scores',
        component: () => import('@/views/scores/index.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
