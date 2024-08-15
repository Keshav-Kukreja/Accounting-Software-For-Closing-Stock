import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
// import router from './router'
import VueCookies from 'vue-cookies'
// import { createRouter, createWebHistory } from 'vue-router'

import router from './router/index.js' // Import the router from your router/index.js

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueCookies);
app.mount('#app')
