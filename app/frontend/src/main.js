// Lib imports
import { createApp } from 'vue';
import { createPinia } from 'pinia';

// App imports
import App from './app.vue';
import router from './router';

createApp(App)
  .use(router)
  .use(createPinia())
  .mount('#app');
