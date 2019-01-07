import Vue from 'vue'
import App from './App.vue'
import router from './router'
import graphql from './graphql'

Vue.config.productionTip = false

new Vue({
  router,
  graphql,
  render: h => h(App)
}).$mount('#app')
