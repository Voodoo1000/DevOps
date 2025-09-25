import { createApp } from 'vue'
import { createPinia } from 'pinia'
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-icons/font/bootstrap-icons.min.css"
import "bootstrap/dist/js/bootstrap"
import "bootstrap/dist/js/bootstrap.bundle.min.js"
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import App from './App.vue'
import router from './router'
import Toast, { POSITION } from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast, {
	position: POSITION.TOP_RIGHT,
});
app.mount('#app')
