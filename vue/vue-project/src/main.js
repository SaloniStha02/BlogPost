import { createApp } from 'vue'
import App from './App.vue'
import router from './route';
import axios from 'axios'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import './assets/style.css';
axios.defaults.baseURL=''
const app = createApp(App);
app.use(Toast)
app.use(router);
app.mount('#app')
