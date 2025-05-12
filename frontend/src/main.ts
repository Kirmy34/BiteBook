import { createApp } from 'vue'
import './style.css'
import router from "./router";
import Toast, { type PluginOptions } from "vue-toastification";
import "vue-toastification/dist/index.css";
import App from './App.vue'

const options: PluginOptions = {
    transition: "Vue-Toastification__fade",
    maxToasts: 20,
    newestOnTop: false,
    position: "bottom-center",
    timeout: false,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: true,
    closeButton: "button",
    icon: true,
    rtl: false
};

const app = createApp(App);

app.use(router);
app.use(Toast, options)

app.mount("#app");