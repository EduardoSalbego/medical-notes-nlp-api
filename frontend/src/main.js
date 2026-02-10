import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Login from './views/Login.vue'
import Dashboard from './views/Dashboard.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/login', component: Login, name: 'Login' },
        { path: '/', component: Dashboard, name: 'Dashboard' }
    ]
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    if (to.name !== 'Login' && !token) next({ name: 'Login' })
    else next()
})

createApp(App)
    .use(createPinia())
    .use(router)
    .mount('#app')